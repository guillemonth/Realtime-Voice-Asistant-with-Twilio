import os 
from dotenv import load_dotenv
load_dotenv()

class GoogleConstants():
    
    LANGUAGE: str = os.environ.get("GOOGLE_LANGUAGE", "es-ES")
    VOICE: str = os.environ.get("GOOGLE_VOICE_ID", "Kore")
    PROJECT_ID: str = os.environ.get("PROJECT_ID", "")
    LOCATION: str = os.environ.get("GOOGLE_LOCATION", "global")
    MODEL: str = os.environ.get("MODEL", "gemini-live-2.5-flash")

    AAD_START_SENS: str = os.environ.get("AAD_START_SENS","")
    AAD_END_SENS: str = os.environ.get("AAD_END_SENS","")
    AAD_PREFIX_MS: str = os.environ.get("AAD_PREFIX_MS","")
    AAD_SILENCE_MS: str = os.environ.get("AAD_SILENCE_MS","")
    AAD_START_ACTIVITY: str = os.environ.get("AAD_START_ACTIVITY","START_OF_ACTIVITY_INTERRUPTS")
    SYSTEM_PROMPT: str = os.environ.get("SYSTEM_PROMPT","")

    #Service Account Info
    PRIVATE_KEY_ID:str = os.environ.get("PRIVATE_KEY_ID","")
    PRIVATE_KEY:str = os.environ.get("PRIVATE_KEY","")
    CLIENT_EMAIL:str = os.environ.get("CLIENT_EMAIL","")
    CLIENT_ID:str = os.environ.get("CLIENT_ID","")
    CLIENT_X509_CERT_URL:str = os.environ.get("CLIENT_X509_CERT_URL","")

    GEMINI_INPUT_RATE:int  = int(os.environ.get("GEMINI_INPUT_RATE",16000))
    GEMINI_OUTPUT_RATE:int  = int(os.environ.get("GEMINI_OUTPUT_RATE",24000))

google_constants = GoogleConstants()