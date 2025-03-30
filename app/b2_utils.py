import environ
from b2sdk.v2 import InMemoryAccountInfo, B2Api

# Load environment variables using django-environ
env = environ.Env()
environ.Env.read_env()

# Initialize Backblaze B2 API
info = InMemoryAccountInfo()
b2_api = B2Api(info)

# Authorize Backblaze B2
b2_api.authorize_account(
    "production",
    env("B2_ACCOUNT_ID"),  # Get from .env using django-environ
    env("B2_APPLICATION_KEY")  # Get from .env using django-environ
)

# Get the bucket object
bucket = b2_api.get_bucket_by_name(env("B2_BUCKET_NAME"))


def upload_file(file, file_name):
    """
    Uploads a file to Backblaze B2 and returns its URL and file ID.
    """
    uploaded_file = bucket.upload_bytes(file.read(), file_name)

    file_url = f"https://{env('B2_BUCKET_NAME')}.s3.us-west-002.backblazeb2.com/{file_name}"
    
    return file_url, uploaded_file.id_


def delete_file(file_id):
    """
    Deletes a file from Backblaze B2 using its ID.
    """
    bucket.delete_file_version(file_id, file_id)
