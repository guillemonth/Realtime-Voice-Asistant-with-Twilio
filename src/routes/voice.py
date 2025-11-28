from fastapi import APIRouter, Request
from fastapi.responses import Response
from src.constants.general_constants import Constants

constants = Constants()
router = APIRouter()

@router.post("/voice")
async def twiml(request: Request):
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <Stream url="wss://{constants.BASE_URL}/ws"/>
  </Connect>
</Response>""".strip()
    return Response(
        content= content,
        media_type="application/xml",
        status_code= 200
    ) 