import httpx
import logging
from app.utils.config import settings

logger = logging.getLogger(__name__)

import json
import os

TOKEN_FILE = "sf_token.json"

async def get_salesforce_token() -> str:
    """Reads the token gained from the web popup flow"""
    if not os.path.exists(TOKEN_FILE):
        raise ValueError("Token missing! You must open http://localhost:8000/auth/salesforce/login in your browser first to click Allow Settings!")
        
    with open(TOKEN_FILE, "r") as f:
        data = json.load(f)
        return data["access_token"]

async def push_to_salesforce(meeting_id: str, transcript: str, insights: dict, recording_url: str):
    """
    Pushes processed call data robustly to Salesforce REST APIs using raw machine-to-machine OAuth setup
    """
    logger.info(f"Pushing data to Salesforce for meeting {meeting_id}")
    
    try:
        access_token = await get_salesforce_token()
    except Exception as e:
        logger.error(f"Could not get Salesforce access token: {e}")
        raise e
    
    base_url = settings.SALESFORCE_INSTANCE_URL.rstrip('/').replace("-setup", "")
    url = f"{base_url}/services/data/v58.0/sobjects/Opportunity/"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Store everything cleanly inside the standard Opportunity Description field
    description_text = f"AI Sentiment: {insights.get('sentiment', 'neutral').upper()}\n"
    description_text += f"Recording URL: {recording_url}\n\n"
    description_text += f"-- CLINICAL SUMMARY --\n{insights.get('summary', '')}"
    
    if insights.get("action_items"):
        actions_text = "\n".join([f"- {item}" for item in insights["action_items"]])
        description_text += f"\n\n-- ACTION ITEMS --\n{actions_text}"
        
    safe_description = description_text if len(description_text) < 32000 else description_text[:31000] + "...(truncated)"
    
    payload = {
        "Name": f"Call Intelligence: {meeting_id}",
        "StageName": "Prospecting",
        "CloseDate": "2024-12-31",
        "Description": safe_description
    }
        
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        
        if response.status_code not in (200, 201, 204):
            logger.error(f"Salesforce error: {response.text}")
            response.raise_for_status()
            
        logger.info(f"Successfully pushed to Salesforce Native App: {response.json()}")
        return response.json()
