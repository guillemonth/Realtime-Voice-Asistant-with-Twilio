import json
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from constants.general_constants import Constants

constants = Constants()
router = APIRouter()

@router.websocket("/ws")
async def media_stream(ws: WebSocket):
    await ws.accept()
    try:
        async for data in ws.iter_json():
            if data["event"] == "start":
                pass
            elif data["event"] == "stop":
                pass
            elif data["event"] == "media":
                media_info: dict = data["media"]
                audio_bytes = media_info["payload"]
                print(f"audio_bytes => {audio_bytes}")
                pass
            # await ws.send_text(f"Echo: {data}")
            # print(data)
    except WebSocketDisconnect:
        print("Llamada finalizada")