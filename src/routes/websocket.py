import asyncio
import base64
import json
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from src.constants.general_constants import Constants
from src.clients.google_client import build_google_client
from src.services.google_to_twilio import forward_google_to_twilio
from src.services.twilio_to_google import forward_twilio_to_google

constants = Constants()
router = APIRouter()

@router.websocket("/ws")
async def media_stream(ws: WebSocket):
    await ws.accept()
    try:

        g_client, g_model, g_config = await build_google_client()
        async with g_client.aio.live.connect(model=g_model, config=g_config) as gws: # type: ignore
            call_data = {}
            t1 = asyncio.create_task(forward_twilio_to_google(ws, gws,call_data))
            t2 = asyncio.create_task(forward_google_to_twilio(ws, gws,call_data))
            done, pending = await asyncio.wait({t1, t2}, return_when=asyncio.FIRST_COMPLETED)
                    # await ws.send_text(f"Echo: {data}")
                    # print(data)
    except WebSocketDisconnect:
        print("Llamada finalizada")
        await ws.close()