from src.routes.voice import router as voice_router

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

app.include_router(voice_router)

@app.get("/")
async def root():
    return JSONResponse(
        content={
            "status": "ok",
            "mensaje": "funciona todo ok"
        },
        status_code=200
    )

@app.get("/")
async def root():
    return JSONResponse(
        content={
            "status": "ok",
            "mensaje": "funciona todo ok"
        },
        status_code=200
    )