from django.shortcuts import render, redirect
import boto3
import os
from django.core.files.storage import default_storage
from b2sdk.v2 import B2Api, InMemoryAccountInfo
from botocore.client import Config
from django.core.exceptions import SuspiciousFileOperation
from django.conf import settings
from django.core.files import File
from app.models import UploadedImage
from .forms import ImageUploadForm
from django.http import JsonResponse
import tempfile

def list_images(request):
    all_images = UploadedImage.objects.all()

    return render(request, 'app/image_list.html', {'all_images':all_images})

def upload_image(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form to get the image object
            image = form.save()

            # Initialize Backblaze B2 API
            info = InMemoryAccountInfo()
            b2_api = B2Api(info)

            # Authorize the account with Backblaze
            b2_api.authorize_account("production", os.environ.get('B2_ACCOUNT_ID'), os.environ.get('B2_APPLICATION_KEY'))

            # Get the bucket
            bucket = b2_api.get_bucket_by_name(os.environ.get('B2_BUCKET_NAME'))

            # Temporarily save the file to disk
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                # Read the file contents
                for chunk in image.image.chunks():
                    tmp_file.write(chunk)
                tmp_file.close()  # Close the file to save it to disk

                # Now, upload this temporary file to Backblaze
                file_info = bucket.upload_local_file(
                    local_file=tmp_file.name,  # Use the file path of the temporary file
                    file_name=str(image.image.name),
                    content_type='application/octet-stream',  # Adjust content type if necessary
                )

            # Optionally remove the temporary file after uploading
            os.remove(tmp_file.name)

            # Get the file URL
            file_url = f"https://{os.environ.get('B2_BUCKET_NAME')}.s3.us-west-002.backblazeb2.com/{image.image.name}"

            # Redirect to a success page with the file URL
            return redirect("upload_success")
    else:
        form = ImageUploadForm()

    return render(request, "app/upload.html", {"form": form})

def upload_success(request):
    return render(request, "app/success.html")
