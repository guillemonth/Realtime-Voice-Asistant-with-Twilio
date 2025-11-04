from fastapi import APIRouter, Request
from fastapi.responses import Response

router = APIRouter()

@router.post("/voice")
async def twiml(request: Request):
    return Response(
        content="<test>Funciona!</test>",
        status_code=200
    ) 