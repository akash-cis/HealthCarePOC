import httpx
import json
from app.utils.config import settings

def test_composio_api():
    url = "https://backend.composio.dev/api/v1/actions"
    headers = {
        "x-api-key": settings.COMPOSIO_API_KEY
    }
    r = httpx.get(url, headers=headers)
    print(f"Status Code: {r.status_code}")
    print(f"Response: {r.text[:500]}")

test_composio_api()
