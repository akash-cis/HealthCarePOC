from fastapi import APIRouter, Header, HTTPException, Request, BackgroundTasks
import logging
import os
import hashlib
import hmac

from app.models.schemas import ZoomWebhookRequest
from app.utils.config import settings
from app.services.zoom_service import download_recording
from app.services.s3_service import upload_to_s3
from app.services.transcription_service import transcribe_audio
from app.services.groq_service import process_transcript
from app.services.salesforce_service import push_to_salesforce

router = APIRouter()
logger = logging.getLogger(__name__)

async def process_recording_pipeline(payload: ZoomWebhookRequest):
    """Background task to process the whole pipeline"""
    meeting_id = str(payload.payload.object.id)
    topic = payload.payload.object.topic
    
    recording_files = payload.payload.object.recording_files
    audio_file_info = next((f for f in recording_files if f.file_extension.upper() == 'M4A'), None)
    
    if not audio_file_info:
        audio_file_info = next((f for f in recording_files if f.file_extension.upper() == 'MP4'), None)
        
    if not audio_file_info:
        logger.warning(f"No suitable audio/video file found for meeting {meeting_id}")
        return

    try:
        # 1. Download Recording
        download_url = audio_file_info.download_url
        download_token = payload.download_token
        
        logger.info(f"Starting pipeline for meeting: {meeting_id} - {topic}")
        local_file_path = await download_recording(download_url, download_token)
        
        # 2. Skip S3 Upload for testing
        s3_url = f"http://localhost:8000/{local_file_path}"
        
        # 3. Transcription (Whisper)
        transcript = await transcribe_audio(local_file_path)
        
        # 4. Claude AI Processing
        insights = await process_transcript(transcript)
        
        # 5. Push to Salesforce
        await push_to_salesforce(meeting_id, transcript, insights, s3_url)
        
        logger.info(f"Pipeline completed successfully for meeting {meeting_id}")
        
    except Exception as e:
        logger.error(f"Error in recording pipeline: {str(e)}", exc_info=True)
    # Skipping the finally cleanup block to preserve the file locally for testing

@router.post("/zoom")
async def zoom_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_zm_signature: str = Header(None),
    x_zm_request_timestamp: str = Header(None)
):
    """
    Receives Zoom recording.completed webhooks.
    """
    body = await request.body()
    
    if not isinstance(body, bytes):
        body = body.encode('utf-8')
        
    try:
        payload_json = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Zoom endpoint URL validation
    if payload_json.get("event") == "endpoint.url_validation":
        plain_token = payload_json.get("payload", {}).get("plainToken")
        if plain_token:
            hash_for_validate = hmac.new(
                settings.ZOOM_WEBHOOK_SECRET.encode('utf-8'),
                plain_token.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            return {
                "plainToken": plain_token,
                "encryptedToken": hash_for_validate
            }

    # Verify Zoom signature
    if settings.ZOOM_WEBHOOK_SECRET and x_zm_signature and x_zm_request_timestamp:
        message = f"v0:{x_zm_request_timestamp}:{body.decode('utf-8')}"
        expected_signature = "v0=" + hmac.new(
            settings.ZOOM_WEBHOOK_SECRET.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        if expected_signature != x_zm_signature:
            logger.warning("Invalid Zoom signature")
            raise HTTPException(status_code=401, detail="Invalid signature")

    if payload_json.get("event") != "recording.completed":
        return {"status": "ignored", "reason": "Event not processing"}
        
    try:
        webhook_data = ZoomWebhookRequest(**payload_json)
        background_tasks.add_task(process_recording_pipeline, webhook_data)
        logger.info(f"Queued background processing for meeting {webhook_data.payload.object.id}")
    except Exception as e:
        logger.error(f"Failed to parse webhook: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload structure")

    return {"status": "success", "message": "Webhook received and queued"}
