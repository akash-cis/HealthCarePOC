import httpx
import logging
import json
from app.utils.config import settings

logger = logging.getLogger(__name__)

async def process_transcript(transcript: str) -> dict:
    """
    Sends transcript to Claude API for summarization and insights.
    Returns a dictionary with summary, sentiment, and action_items.
    """
    logger.info("Processing transcript with Claude API")
    
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": settings.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    prompt = f"""
    Please analyze the following call transcript and provide a JSON response. Do not include any other text besides the JSON.
    
    Transcript:
    \"\"\"{transcript}\"\"\"
    
    Return exactly this JSON format:
    {{
        "summary": "Brief summary of the call",
        "sentiment": "positive | neutral | negative",
        "action_items": ["item 1", "item 2"]
    }}
    """
    
    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1024,
        "temperature": 0.2,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result_content = response.json().get("content", [{}])[0].get("text", "")
        
        try:
            if "```json" in result_content:
                result_content = result_content.split("```json")[1].split("```")[0].strip()
            elif "```" in result_content:
                result_content = result_content.split("```")[1].split("```")[0].strip()
                
            parsed_data = json.loads(result_content)
            logger.info("Claude processing completed.")
            return parsed_data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response as JSON: {result_content}")
            raise e
