from composio import ComposioToolSet, Action
from app.utils.config import settings
import json

try:
    toolset = ComposioToolSet(api_key=settings.COMPOSIO_API_KEY)
    action = toolset.get_action(Action.SALESFORCE_CREATE_RECORD)
    print(json.dumps(action.schema, indent=2))
except Exception as e:
    print(f"Error fetching schema: {e}")
