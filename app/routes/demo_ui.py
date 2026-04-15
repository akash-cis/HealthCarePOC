from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import httpx
import os
import json
import logging
import re
from app.utils.config import settings
from app.services.salesforce_service import push_to_salesforce

router = APIRouter()
logger = logging.getLogger(__name__)

class ProcessRequest(BaseModel):
    transcript: str

class PushRequest(BaseModel):
    transcript: str
    insights: dict

def load_js_string(filepath):
    """Fallback helper to extract strings from JS mock files"""
    if not os.path.exists(filepath):
        return "ERROR: mock file not found locally"
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'`(.*?)`', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

@router.get("/", response_class=HTMLResponse)
async def serve_ui():
    """Serves the beautiful UI application page"""
    html_path = os.path.join(os.path.dirname(__file__), "..", "templates", "index.html")
    if not os.path.exists(html_path):
        return HTMLResponse("<h1>Template not found. Check app/templates/index.html</h1>", status_code=404)
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@router.get("/api/demo/transcript")
async def get_transcript():
    transcript_path = os.path.join(os.path.dirname(__file__), "..", "..", "without zoom demo files", "mock-healthcare-transcript.js")
    transcript = load_js_string(transcript_path)
    return {"transcript": transcript}

@router.post("/api/demo/summarize")
async def summarize_call(req: ProcessRequest):
    logger.info("Executing Web Demo summarize hook")
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "..", "without zoom demo files", "healthcare-prompt.js")
    prompt_template = load_js_string(prompt_path)
    
    full_prompt = prompt_template.replace("{TRANSCRIPT_HERE}", req.transcript)
    full_system_prompt = """You are an advanced clinical documentation AI.
CRITICAL JSON REQUIREMENT:
You must output a raw, parseable JSON object. The detailed clinical markdown summary you generate MUST be entirely contained within the "summary" key.
Format:
{
    "summary": "YOUR ENTIRE MARKDOWN OUTPUT GOES HERE (use \\n for proper line breaks and ## for headers)",
    "sentiment": "positive | neutral | negative",
    "action_items": ["Array", "of", "high", "priority", "action", "items"]
}"""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": full_system_prompt},
            {"role": "user", "content": full_prompt}
        ]
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Groq API failed")
            
        result_content = response.json()["choices"][0]["message"]["content"]
        insights = json.loads(result_content)
        return {"insights": insights}

@router.post("/api/demo/push")
async def push_to_sf(req: PushRequest):
    logger.info("Pushing web UI demo data to Salesforce Opportunity")
    try:
        meeting_id = "WEB-DEMO-UI-102"
        mock_s3_url = "http://demo-storage.hospital.local/handoffs/april-15.m4a"
        await push_to_salesforce(meeting_id, req.transcript, req.insights, mock_s3_url)
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Push failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
