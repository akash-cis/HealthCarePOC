import boto3
import logging
from botocore.exceptions import ClientError
from app.utils.config import settings

logger = logging.getLogger(__name__)

def upload_to_s3(file_path: str, object_name: str) -> str:
    """
    Uploads a file to AWS S3 and returns the public URL.
    """
    logger.info(f"Uploading {file_path} to S3 bucket {settings.AWS_BUCKET_NAME} as {object_name}")
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
    
    try:
        s3_client.upload_file(file_path, settings.AWS_BUCKET_NAME, object_name)
    except ClientError as e:
        logger.error(f"Failed to upload to S3: {e}")
        raise e
        
    url = f"https://{settings.AWS_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{object_name}"
    logger.info(f"Uploaded successfully. URL: {url}")
    return url
