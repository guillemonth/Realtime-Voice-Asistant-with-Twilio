import audioop
import numpy as np
# from scipy import signal
import librosa
from src.constants.google_constants import GoogleConstants
from src.constants.general_constants import Constants

constans = Constants()
g_constants = GoogleConstants()

async def ulaw8k_to_pcm16k(ulaw_bytes: bytes) -> bytes:
    """Convert μ-law 8kHz to PCM 16kHz for Gemini."""
    pcm_8k = audioop.ulaw2lin(ulaw_bytes, 2)
    pcm_16k, _ = audioop.ratecv(pcm_8k, 2, 1, constans.TWILIO_OUTPUT_RATE, g_constants.GEMINI_INPUT_RATE, None) # type: ignore
    return pcm_16k

async def pcm16k_to_ulaw8k(buffer) -> bytes:
    """"""
    sample_width = 2  # PCM16 -> 2 bytes per sample
    
    pcm_8k, _ = audioop.ratecv(buffer, sample_width, 1, g_constants.GEMINI_INPUT_RATE, constans.TWILIO_OUTPUT_RATE, None)
    ulaw_bytes = audioop.lin2ulaw(pcm_8k, sample_width)
    return ulaw_bytes



# --- Mu-Law Encoding Function ---
# Note: This is a standard implementation of the u-law/mu-law algorithm
# Mu-law is a logarithmic compression algorithm (A-law is common in Europe, Mu-law in North America/Japan)
def pcm_to_mulaw(pcm_data, mu=255):
    """
    Encodes 16-bit linear PCM data to 8-bit mu-law data.

    Args:
        pcm_data (np.ndarray): 16-bit PCM audio array (e.g., from an audio stream).
        mu (int): The mu-law parameter. Standard is 255.

    Returns:
        np.ndarray: 8-bit mu-law encoded array.
    """
    # 1. Normalize the PCM data to [-1, 1] (required for the algorithm)
    # The max value for a signed 16-bit integer is 32767
    normalized = pcm_data.astype(np.float64) / 32768.0

    # 2. Apply the mu-law formula: sign(x) * (ln(1 + mu*|x|) / ln(1 + mu))
    encoded = np.sign(normalized) * (np.log(1 + mu * np.abs(normalized)) / np.log(1 + mu))

    # 3. Quantize to 8 bits (0-255) and cast to unsigned 8-bit integer (uint8)
    # The output values are in [-1, 1]. Map them to [0, 255].
    mulaw_bytes = ((encoded + 1) / 2 * 255).astype(np.uint8)

    return mulaw_bytes

# --- Main Conversion Function ---
def convert_pcm_16k_to_mulaw_8k(pcm_chunk, input_samplerate=16000, output_samplerate=8000):
    """
    Converts a chunk of 16 kHz, 16-bit linear PCM audio to 8 kHz, 8-bit mu-law.

    Args:
        pcm_chunk (bytes): Raw audio bytes from your stream. Assuming little-endian.
        input_samplerate (int): The current sample rate (16000 Hz).
        output_samplerate (int): The desired sample rate (8000 Hz).

    Returns:
        bytes: The 8 kHz mu-law encoded raw audio bytes.
    """
    if len(pcm_chunk) % 2 != 0:
        print(f"⚠️ Warning: Buffer size is odd ({len(pcm_chunk)} bytes). Truncating the last byte.")
        # Safely remove the last byte to make the buffer size even
        # This prevents the error and only loses 1 byte (half a sample)
        pcm_chunk = pcm_chunk[:-1]
        
        # If after truncating, the chunk is empty, return
        if not pcm_chunk:
            return b''

    # 1. Convert raw bytes (chunk) to a numpy array (16-bit integers)
    # Assuming the incoming stream is 16-bit signed little-endian PCM
    # The resulting array will be a sequence of 16-bit (np.int16) samples
    try:
        audio_array = np.frombuffer(pcm_chunk, dtype=np.int16)
    except ValueError as e:
        print(f"Error converting bytes to np.int16: {e}")
        return b''

    # 2. Resample the audio from 16 kHz to 8 kHz
    # librosa's resampling is generally faster and higher quality than scipy.signal.resample
    # if you are dealing with music/speech.
    
    resampled_array = librosa.resample(
        y=audio_array.astype(np.float32), 
        orig_sr=input_samplerate, 
        target_sr=output_samplerate, 
        res_type='kaiser_best' # High-quality filter
    )
    
    # Resample will output float32, we need to convert it back to int16 for mu-law encoding input
    # Scale back to the range of 16-bit signed integers
    resampled_int16 = np.clip(resampled_array * 32767, -32768, 32767).astype(np.int16)

    # 3. Apply Mu-law encoding
    mulaw_array = pcm_to_mulaw(resampled_int16)

    # 4. Convert the resulting numpy array (uint8) back to raw bytes for API transmission
    return mulaw_array.tobytes()

# --- Example Usage ---
# Assume you receive a chunk of raw 16-bit PCM data (e.g., 20ms = 320 samples * 2 bytes/sample = 640 bytes)
# Create a dummy chunk of silence (320 samples of 16-bit zero)
dummy_pcm_chunk = np.zeros(320, dtype=np.int16).tobytes()

mulaw_bytes_8k = convert_pcm_16k_to_mulaw_8k(dummy_pcm_chunk)

print(f"Original PCM chunk size: {len(dummy_pcm_chunk)} bytes (16-bit, 16kHz)")
print(f"Converted Mu-law chunk size: {len(mulaw_bytes_8k)} bytes (8-bit, 8kHz)")
print(f"Expected size for 20ms: 0.02s * 8000 samples/s * 1 byte/sample = 160 bytes")