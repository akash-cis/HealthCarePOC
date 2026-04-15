import httpx
import logging
import tempfile
import base64
from app.utils.config import settings

logger = logging.getLogger(__name__)

async def get_zoom_access_token() -> str:
    """Get Server-to-Server OAuth token for Zoom"""
    url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={settings.ZOOM_ACCOUNT_ID}"
    auth_str = f"{settings.ZOOM_CLIENT_ID}:{settings.ZOOM_CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {b64_auth}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers)
        response.raise_for_status()
        return response.json()["access_token"]

async def download_recording(download_url: str, download_token: str) -> str:
    """
    Downloads the recording from Zoom and saves it to a temporary file.
    Returns the path to the downloaded file.
    """
    logger.info(f"Downloading recording from {download_url}")
    
    # Prefer S2S token if credentials provided, otherwise fallback to download_token
    token = download_token
    if settings.ZOOM_ACCOUNT_ID and settings.ZOOM_CLIENT_ID:
        try:
            token = await get_zoom_access_token()
        except Exception as e:
            logger.warning(f"Failed to get S2S token, falling back to download_token: {e}")
    
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    import os
    os.makedirs("local_recordings", exist_ok=True)
    file_path = f"local_recordings/recording_{os.urandom(4).hex()}.m4a"

    async with httpx.AsyncClient() as client:
        async with client.stream("GET", download_url, headers=headers, follow_redirects=True) as response:
            response.raise_for_status()
            with open(file_path, "wb") as f:
                async for chunk in response.aiter_bytes():
                    f.write(chunk)
                    
    logger.info(f"Recording downloaded to {file_path}")
    return file_path
