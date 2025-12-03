import logging
import os
from typing import Dict, Optional
from google import genai
from google.genai import types as gtypes
from google.oauth2 import service_account
from src.constants.google_constants import google_constants as g_constants

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # asegura que los INFO se impriman al ejecutar el script directamente

async def build_google_client():
    """
    Context manager yielding a session adapter backed by the Google SDK.

    Uses Vertex AI with service account credentials from a JSON file, mirroring
    the approach in liveapi_sdk_example_speech.py. If the credentials file is
    not found, falls back to API‑key mode for development convenience.
    """

    client = None

    
    sa_info = build_sa_info()
    if sa_info is None:
        raise RuntimeError("No Service Account Info was found")
    
    try:
        project_id = g_constants.PROJECT_ID
        if not project_id:
            raise RuntimeError("Project ID is required for Vertex AI connection")

        creds = service_account.Credentials.from_service_account_info(
            sa_info,
            scopes= ["https://www.googleapis.com/auth/cloud-platform"],
        ).with_quota_project(project_id)
        
        # custom http options for solving keepalive error
        http_opts = gtypes.HttpOptions(
            async_client_args={
                "ping_interval": 10,
                "ping_timeout": 60,
                "close_timeout": 20,
                "open_timeout": 15,
                "max_queue": 32
            }
        )

        client = genai.Client(
            vertexai= True,
            project= project_id,
            location= g_constants.LOCATION,
            credentials= creds,
            http_options= http_opts
        )
    except Exception as exc:
        log.warning("Failed to init Vertex AI client from env SA info: %s", exc)

    realtime_input_config = {
        "automatic_activity_detection": {
            "disabled": False,
            "start_of_speech_sensitivity": g_constants.AAD_START_SENS,
            "end_of_speech_sensitivity": g_constants.AAD_END_SENS,
            "prefix_padding_ms": g_constants.AAD_PREFIX_MS,
            "silence_duration_ms": g_constants.AAD_SILENCE_MS,
        },
        "activity_handling": g_constants.AAD_START_ACTIVITY
    }

    config = {
        "response_modalities": ["AUDIO"],
        "system_instruction": {
            "role": "user",
            "parts": [{"text": g_constants.SYSTEM_PROMPT}],
        },
        # Realtime behavior
        "realtime_input_config": realtime_input_config,
        "input_audio_transcription" : {},
        "output_audio_transcription" : {},
        "speech_config": {
            "voice_config": {
                "prebuilt_voice_config": {"voice_name": g_constants.VOICE}
            },
            "language_code":g_constants.LANGUAGE
        }
    }
    return client, g_constants.MODEL, config
    

def build_sa_info() -> Optional[Dict[str, str]]:
    """Build a service-account info dict from environment variables.

    Returns a dict compatible with
    google.oauth2.service_account.Credentials.from_service_account_info,
    or None if required variables are missing.
    """

    log.info("entra a la función")

    project_id = g_constants.PROJECT_ID
    private_key_id = g_constants.PRIVATE_KEY_ID
    private_key = g_constants.PRIVATE_KEY
    client_email = g_constants.CLIENT_EMAIL
    client_id = g_constants.CLIENT_ID
    client_x509_cert_url = g_constants.CLIENT_X509_CERT_URL

    required = [
        project_id,
        private_key_id,
        private_key,
        client_email,
        client_id,
        client_x509_cert_url,
    ]

    if not all(required):
        return None

    # Normalize escaped newlines in PRIVATE_KEY if provided via .env
    if "\\n" in private_key:
        private_key = private_key.replace("\\n", "\n")

    info: Dict[str, str] = {
        "type": "service_account",
        "project_id": project_id,
        "private_key_id": private_key_id,
        "private_key": private_key,
        "client_email": client_email,
        "client_id": client_id,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": client_x509_cert_url,
        "universe_domain": "googleapis.com",
    }
    return info