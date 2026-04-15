import httpx
import logging
import os
from app.utils.config import settings

logger = logging.getLogger(__name__)

async def transcribe_audio(file_path: str) -> str:
    """
    Sends audio file to Groq Whisper API for lightning-fast transcription.
    """
    logger.info(f"Transcribing audio file via Groq Whisper API, path: {file_path}")
    
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}"
    }
    
    with open(file_path, "rb") as audio_file:
        files = {
            "file": (os.path.basename(file_path), audio_file, "audio/mp4")
        }
        data = {
            "model": "whisper-large-v3-turbo", 
            "response_format": "text",
            "language": "en"
        }
        
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(url, headers=headers, files=files, data=data)
            if response.status_code != 200:
                logger.error(f"Groq Whisper error: {response.text}")
                response.raise_for_status()
            
            transcript = response.text
            logger.info("Transcription completed successfully via Groq.")
            return transcript
