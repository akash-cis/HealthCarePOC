from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import httpx
import json
import logging
import hashlib
import base64
import secrets
from app.routes import webhook, demo_ui
from app.utils.config import settings

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = FastAPI(
    title="Call Intelligence Pipeline POC",
    description="Processes Zoom recordings, transcribes them, extracts insights, and pushes to Salesforce.",
    version="1.0.0"
)

# Include routers
app.include_router(demo_ui.router, tags=["demo-ui"])
app.include_router(webhook.router, prefix="/webhook", tags=["webhooks"])

# Global store for PKCE token passing
pkce_store = {}

@app.get("/auth/salesforce/login")
def salesforce_login():
    """Redirects your browser to the Salesforce login screen"""
    # Generate PKCE verifier and challenge
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).decode('utf-8').rstrip('=')
    
    pkce_store['verifier'] = code_verifier
    
    url = (
        f"https://login.salesforce.com/services/oauth2/authorize"
        f"?response_type=code"
        f"&client_id={settings.SALESFORCE_CONSUMER_KEY}"
        f"&redirect_uri=http://localhost:8000/auth/salesforce/callback"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method=S256"
    )
    return RedirectResponse(url)

@app.get("/auth/salesforce/callback")
async def salesforce_callback(code: str):
    """Salesforce sends the code here after you click 'Allow' in the browser"""
    token_url = "https://login.salesforce.com/services/oauth2/token"
    
    payload = {
        "grant_type": "authorization_code",
        "client_id": settings.SALESFORCE_CONSUMER_KEY,
        "client_secret": settings.SALESFORCE_CONSUMER_SECRET,
        "redirect_uri": "http://localhost:8000/auth/salesforce/callback",
        "code": code,
        "code_verifier": pkce_store.get("verifier", "")
    }
    
    async with httpx.AsyncClient() as client:
        r = await client.post(token_url, data=payload)
        if r.status_code == 200:
            with open("sf_token.json", "w") as f:
                json.dump(r.json(), f)
            return {"message": "Success! Token securely saved. You can close this browser window and run `python run_demo.py` in your terminal now!"}
        else:
            return {"error": "Failed to get token", "details": r.text}
