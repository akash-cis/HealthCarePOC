from pydantic import BaseModel
from typing import Optional, List

class ZoomRecordingFile(BaseModel):
    id: str
    meeting_id: str = ""
    file_extension: str
    download_url: str
    # Other zoom recording attributes can be expanded here

class ZoomPayloadObject(BaseModel):
    id: int
    topic: str
    recording_files: List[ZoomRecordingFile]

class ZoomWebhookPayload(BaseModel):
    object: ZoomPayloadObject

class ZoomWebhookRequest(BaseModel):
    event: str
    payload: ZoomWebhookPayload
    download_token: Optional[str] = None
