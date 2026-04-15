import httpx
import logging
import json
from app.utils.config import settings

logger = logging.getLogger(__name__)

async def process_transcript(transcript: str) -> dict:
    """
    Sends transcript to Groq LLaMA-based API for summarization and insights.
    Returns a dictionary with summary, sentiment, and action_items.
    """
    logger.info("Processing transcript with Groq LLaMA models")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
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
        "model": "llama-3.3-70b-versatile",
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": "You are a helpful assistant designed to output pure JSON."},
            {"role": "user", "content": prompt}
        ]
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code != 200:
            logger.error(f"Groq API error: {response.text}")
            response.raise_for_status()
            
        result_content = response.json()["choices"][0]["message"]["content"]
        
        try:
            parsed_data = json.loads(result_content)
            logger.info("Groq processing completed.")
            return parsed_data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Groq response as JSON: {result_content}")
            raise e
