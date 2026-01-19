import audioop
from src.constants.google_constants import google_constants as g_constants
from src.constants.general_constants import constants


async def ulaw8k_to_pcm16k(ulaw_bytes: bytes) -> bytes:
    """
    Convert μ-law audio at 8kHz to pcm audio at 16kHz
    
    Args:
        buffer (bytes): Audio bytes to convert
    Returns:
        bytes: Converted audio bytes
    """
    pcm_8k = audioop.ulaw2lin(ulaw_bytes, 2)
    pcm_16k, _ = audioop.ratecv(pcm_8k, 2, 1, constans.TWILIO_RATE, g_constants.GEMINI_INPUT_RATE, None) # type: ignore
    return pcm_16k

async def pcm24k_to_ulaw8k(buffer: bytes) -> bytes:
    """
    Convert pcm audio at 24kHz to μ-law audio at 8kHz.
    
    Args:
        buffer (bytes): Audio bytes to convert
    Returns:
        bytes: Converted audio bytes
    """
    pcm_8k, _ = audioop.ratecv(buffer, 2, 1, g_constants.GEMINI_OUTPUT_RATE, constants.TWILIO_RATE, None)
    ulaw_bytes = audioop.lin2ulaw(pcm_8k, 2)
    return ulaw_bytes
