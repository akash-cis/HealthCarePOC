import asyncio
import logging
import json
import httpx
import re
import os
from app.utils.config import settings
from app.services.salesforce_service import push_to_salesforce

# Tidy up logging output for the demo
logging.getLogger("httpx").setLevel(logging.WARNING)

def load_js_string(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'`(.*?)`', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

async def run_healthcare_demo():
    print("\n--- Starting Healthcare Demo Pipeline (Bypassing Zoom) ---")
    
    # Load demo files provided by user
    transcript_path = "without zoom demo files/mock-healthcare-transcript.js"
    prompt_path = "without zoom demo files/healthcare-prompt.js"
    
    if not os.path.exists(transcript_path):
        print(f"ERROR: Could not find {transcript_path}")
        return
        
    transcript = load_js_string(transcript_path)
    prompt_template = load_js_string(prompt_path)
    
    print("Loaded Healthcare Mock Transcript and Prompts...")
    
    # Insert transcript into prompt
    full_prompt = prompt_template.replace("{TRANSCRIPT_HERE}", transcript)
    
    # Construct a System Prompt to cleanly enforce our required JSON architecture
    full_system_prompt = """You are an advanced clinical documentation AI.
    
CRITICAL JSON REQUIREMENT:
You must output a raw, parseable JSON object. The detailed clinical markdown summary you generate based on the user's prompt MUST be entirely contained within the "summary" key. Do NOT wrap the JSON inside markdown blocks like `json ...`.

Format:
{
    "summary": "YOUR ENTIRE MARKDOWN OUTPUT GOES HERE (use \\n for proper line breaks and ## for headers)",
    "sentiment": "positive | neutral | negative",
    "action_items": ["Array", "of", "high", "priority", "action", "items"]
}
"""
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    print("Processing transcript via Groq LLaMA-3.3-70B (Extracting Healthcare Summary)...")
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
            print(f"ERROR: Groq API Error: {response.text}")
            return
            
        result_content = response.json()["choices"][0]["message"]["content"]
        try:
            insights = json.loads(result_content)
            print(f"SUCCESS: Groq Processing Complete! Generated Clinical Summary Length: {len(insights.get('summary', ''))} characters")
        except Exception as e:
            print(f"ERROR: Failed to parse Groq response as JSON: {e}")
            return
    
    meeting_id = "DEMO-CLINICAL-HANDOFF-101"
    mock_s3_url = "http://demo-storage.hospital.local/handoffs/april-15.m4a"
    
    print(f"Pushing to Salesforce Custom Object (Call_Recording__c) for Meeting: {meeting_id}...")
    
    try:
        sf_result = await push_to_salesforce(
            meeting_id=meeting_id,
            transcript=transcript,
            insights=insights,
            recording_url=mock_s3_url
        )
        print("\nSUCCESS: Demo completed securely!")
        print(f"   Check your Salesforce org for a new Call_Recording__c called '{meeting_id}'")
        print("   It will contain the fully mapped AI summary, raw transcript, and action items!")
    except Exception as e:
        print(f"\nERROR: Salesforce Error: {e}")

if __name__ == "__main__":
    asyncio.run(run_healthcare_demo())
