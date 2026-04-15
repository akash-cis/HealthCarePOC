from composio import Composio

try:
    c = Composio(api_key="test-key")
    print("Composio methods:", [m for m in dir(c) if not m.startswith('_')])

    session = c.create(user_id="test")
    print("Session methods:", [m for m in dir(session) if not m.startswith('_')])
except Exception as e:
    print(f"Error inspecting Composio: {e}")
