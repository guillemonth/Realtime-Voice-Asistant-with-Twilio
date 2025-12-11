import base64
import logging
from fastapi import WebSocket
from src.clients.google_client import GoogleSDKSessionAdapter
from src.tools.audio_tools import ulaw8k_to_pcm16k

log = logging.getLogger("twilio_to_google")

async def forward_twilio_to_google(t_ws: WebSocket,g_ws: GoogleSDKSessionAdapter,call_data):
    """
    Receives the messages from Twilio and sends them to Google
    Args:
        t_ws (Websocket): Twilio WebSocket
        g_ws (GoogleSDKSessionAdapter): Google session handler
        call_data (Dict[str,str]): Dictionary with call data
    """
    async for data in t_ws.iter_json():
        if data["event"] == "start":
            log.info(f"se inicia la llamada => {data}")
            start_data = data["start"]
            call_data["stream_sid"] = start_data.get("streamSid")
        elif data["event"] == "stop":
            log.info("se finaliza la llamada")
        elif data["event"] == "media":
            media_info: dict = data["media"]
            audio_bytes = media_info["payload"]
            transformed_audio = await ulaw8k_to_pcm16k(base64.b64decode(audio_bytes))
            await g_ws.send(
                {
                    "mimeType": "audio/pcm;rate=16000",
                    "data": base64.b64encode(transformed_audio).decode()
                }
            )