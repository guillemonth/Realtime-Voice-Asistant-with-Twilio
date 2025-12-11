import base64
import json
import logging
import wave
from typing import List

from fastapi import WebSocket
from google.genai.types import (
    LiveServerContent,
    Content,
    Part,
    Blob,
    Transcription,
)

from src.clients.google_client import GoogleSDKSessionAdapter
from src.tools.audio_tools import pcm24k_to_ulaw8k

log = logging.getLogger("google_to_twilio")

async def forward_google_to_twilio(t_ws: WebSocket,g_ws: GoogleSDKSessionAdapter,call_data):
    """
    Receives the messages from Google and sends them back to Twilio
    
    Args:
        t_ws (Websocket): Twilio WebSocket
        g_ws (GoogleSDKSessionAdapter): Google session handler
        call_data (Dict[str,str]): Dictionary with call data
    """
    
    audio_buffer: bytes = b''
    async for msg in g_ws:
        server_content: LiveServerContent|None = getattr(msg, "server_content", None)
        model_turn:Content|None = getattr(server_content, "model_turn", None) if server_content else None
        parts_list: List[Part]|None = getattr(model_turn, "parts", None) if model_turn else None
        part: Part|None = parts_list[0] if parts_list else None
        inline_data: Blob|None = getattr(part, "inline_data", None) if part else None
        data: bytes|None = getattr(inline_data, "data", None) if inline_data else None

        if not part:
            log.info(f"log de google => {msg}")

        input_transcription_obj: Transcription|None = getattr(server_content, "input_transcription", None) if server_content else None
        input_transcription: str|None = getattr(input_transcription_obj, "text", None) if input_transcription_obj else None
        
        if input_transcription:
            log.info(f"tenemos input_transcription => {input_transcription}")
        
        if data:
            raw_audio: bytes = b''
            try:
                raw_audio = data
                
            except BaseException as e:
                log.error(f"error al decodificar => {e}|| {data}")

            #in case the audio content is empty, we'll wait for the next package
            if len(raw_audio) == 0:
                continue

            audio_buffer += raw_audio

            mulaw_audio: bytes = await pcm24k_to_ulaw8k(audio_buffer)
            audio_buffer = b''

            payload: str = base64.b64encode(mulaw_audio).decode()
            ws_input: str = json.dumps({
                "event": "media",
                "streamSid": call_data.get("stream_sid"),
                "media": {"payload": payload},
            })
            await t_ws.send_text(ws_input)
