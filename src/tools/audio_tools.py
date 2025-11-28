import audioop
from src.constants.google_constants import GoogleConstants
from src.constants.general_constants import Constants

constans = Constants()
g_constants = GoogleConstants()

async def ulaw8k_to_pcm16k(ulaw_bytes: bytes) -> bytes:
    """Convert μ-law 8kHz to PCM 16kHz for Gemini."""
    pcm_8k = audioop.ulaw2lin(ulaw_bytes, 2)
    pcm_16k, _ = audioop.ratecv(pcm_8k, 2, 1, constans.TWILIO_OUTPUT_RATE, g_constants.GEMINI_INPUT_RATE, None) # type: ignore
    return pcm_16k

async def pcm16k_to_ulaw8k(pcm_bytes: bytes,buffer) -> bytes:
    sample_width = 2  # PCM16 -> 2 bytes per sample
    
    buffer += pcm_bytes    
    #In case the amount of bytes is odd, we have to store
    if len(buffer) % 2 == 0:
        return b''
    pcm_8k, _ = audioop.ratecv(buffer, sample_width, 1, g_constants.GEMINI_INPUT_RATE, constans.TWILIO_OUTPUT_RATE, None)
    ulaw_bytes = audioop.lin2ulaw(pcm_8k, sample_width)
    return ulaw_bytes