import asyncio
import base64
import logging
import json
from typing import List
from fastapi import WebSocket
from google.genai.types import LiveServerContent,Content,Part,Blob,Transcription
from src.tools.audio_tools import pcm16k_to_ulaw8k

log = logging.getLogger("google_to_twilio")

async def forward_google_to_twilio(t_ws: WebSocket,g_ws,call_data):
    audio_buffer = b''
    # while True:
        # msg = await g_ws.receive():
    file = open("audio.wav",'ab')
    async for msg in g_ws:
        # msg = json.loads(raw_msg)
        # log.info(f"mensaje recibido de google => {msg}")
        # try:
        #     #Se comprueba que el mensaje de google contenga el audio

        server_content: LiveServerContent|None = getattr(msg, "server_content", None)
        model_turn:Content|None = getattr(server_content, "model_turn", None) if server_content else None
        parts_list: List[Part]|None = getattr(model_turn, "parts", None) if model_turn else None
        part: Part|None = parts_list[0] if parts_list else None
        inline_data: Blob|None = getattr(part, "inline_data", None) if part else None
        data: str|None = getattr(inline_data, "data", None) if inline_data else None

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

            # log.info(f"decoded audio => {raw_audio}")
            audio_buffer += raw_audio # type: ignore
            
            #In case the amount of bytes is odd, we have to store
            # if len(audio_buffer) % 2 != 0:
            #     continue

            mulaw_audio = await pcm16k_to_ulaw8k(audio_buffer)
            # mulaw_audio = convert_pcm_16k_to_mulaw_8k(raw_audio)
            file.write(mulaw_audio)
            audio_buffer = b''

            payload = base64.b64encode(mulaw_audio).decode()
            input = json.dumps({
                "event": "media",
                "streamSid": call_data.get("stream_sid"),
                "media": {"payload": payload},
            })
            await t_ws.send_text(input)
        # except Exception as e:
        #     log.info(f"algo ha petado => {e.with_traceback} || {e.args}")
    log.info("sale del bucle")
    file.close()
    await asyncio.sleep(100)