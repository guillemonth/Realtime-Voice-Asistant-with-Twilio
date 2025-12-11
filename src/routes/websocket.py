import asyncio
from fastapi import (
    APIRouter, 
    WebSocket, 
    WebSocketDisconnect,
)
from src.clients.google_client import connect_google_live
from src.services.google_to_twilio import forward_google_to_twilio
from src.services.twilio_to_google import forward_twilio_to_google

router = APIRouter()

@router.websocket("/ws")
async def media_stream(ws: WebSocket):
    await ws.accept()
    try:
        async with connect_google_live() as gws:
            call_data = {}
            t1 = asyncio.create_task(forward_twilio_to_google(ws, gws,call_data))
            t2 = asyncio.create_task(forward_google_to_twilio(ws, gws,call_data))
            done, pending = await asyncio.wait({t1, t2}, return_when=asyncio.FIRST_COMPLETED)
            
            for task in pending:
                task.cancel()
    except WebSocketDisconnect:
        print("Llamada finalizada")
        await ws.close()