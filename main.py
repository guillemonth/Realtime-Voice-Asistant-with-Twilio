from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.routes.voice import router as voice_router
from src.routes.websocket import router as websocket_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(voice_router)
app.include_router(websocket_router)

@app.get("/")
async def root():
    return JSONResponse(
        content={
            "status": "ok",
            "mensaje": "everything is running smoothly!"
        },
        status_code=200
    )