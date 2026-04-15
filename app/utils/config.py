import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ZOOM_WEBHOOK_SECRET = os.getenv("ZOOM_WEBHOOK_SECRET", "")
    ZOOM_ACCOUNT_ID = os.getenv("ZOOM_ACCOUNT_ID", "")
    ZOOM_CLIENT_ID = os.getenv("ZOOM_CLIENT_ID", "")
    ZOOM_CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET", "")
    
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    
    SALESFORCE_INSTANCE_URL = os.getenv("SALESFORCE_INSTANCE_URL", "")
    SALESFORCE_USERNAME = os.getenv("SALESFORCE_USERNAME", "")
    SALESFORCE_PASSWORD = os.getenv("SALESFORCE_PASSWORD", "")
    SALESFORCE_CONSUMER_KEY = os.getenv("SALESFORCE_CONSUMER_KEY", "")
    SALESFORCE_CONSUMER_SECRET = os.getenv("SALESFORCE_CONSUMER_SECRET", "")

settings = Settings()
