"""
Audio processing module for voice transcription.
Uses Google Speech Recognition API for transcription.
"""
import logging
import io
import speech_recognition as sr
from pydub import AudioSegment
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def convert_webm_to_wav(audio_bytes: bytes) -> bytes:
    """
    Convert WebM audio bytes to WAV format.
    Streamlit audio_input returns WebM format, but speech_recognition needs WAV.
    
    Args:
        audio_bytes: Audio data in bytes (WebM format)
        
    Returns:
        Audio data in WAV format as bytes
    """
    try:
        # Try to detect format automatically first
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        
        # Set sample rate and channels for compatibility
        audio = audio.set_frame_rate(16000).set_channels(1)
        
        # Convert to WAV
        wav_buffer = io.BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_bytes = wav_buffer.getvalue()
        
        return wav_bytes
    except Exception as e:
        logger.warning(f"Auto-format detection failed, trying WebM: {e}")
        try:
            # Try explicitly as WebM
            audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="webm")
            audio = audio.set_frame_rate(16000).set_channels(1)
            wav_buffer = io.BytesIO()
            audio.export(wav_buffer, format="wav")
            wav_bytes = wav_buffer.getvalue()
            return wav_bytes
        except Exception as e2:
            logger.error(f"WebM conversion failed: {e2}", exc_info=True)
            # Return original bytes (might already be WAV)
            return audio_bytes


def transcribe_audio(audio_bytes: bytes) -> Optional[str]:
    """
    Transcribe audio bytes to text using Google Speech Recognition.
    
    Args:
        audio_bytes: Audio data in bytes (WebM or WAV format)
        
    Returns:
        Transcribed text or None if transcription fails
    """
    try:
        # Convert WebM to WAV if needed
        wav_bytes = convert_webm_to_wav(audio_bytes)
        
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Convert bytes to AudioData
        audio_file = io.BytesIO(wav_bytes)
        
        # Read audio file
        with sr.AudioFile(audio_file) as source:
            # Adjust for ambient noise
            try:
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
            except Exception as e:
                logger.warning(f"Could not adjust for ambient noise: {e}")
            
            # Record audio
            audio = recognizer.record(source)
        
        # Transcribe using Google Speech Recognition
        try:
            text = recognizer.recognize_google(audio)
            logger.info(f"Transcription successful: {text}")
            return text
        except sr.UnknownValueError:
            logger.error("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition service: {e}")
            return None
            
    except Exception as e:
        logger.error(f"Error processing audio: {e}", exc_info=True)
        return None
