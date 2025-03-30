import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import ImageUploadForm
from .models import UploadedImage
from .b2_utils import upload_file, delete_file

def upload_image(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            file_name = file.name

            # Check if the environment is development or production
            if os.environ.get("DJANGO_ENV") == "development":
                # Save the file locally in development
                file_name = f"uploads/{file_name}"
                file_url = f"/media/{file_name}"  # Local URL

                # Save the file to the media directory (in the local storage)
                with open(os.path.join(settings.MEDIA_ROOT, file_name), "wb") as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                
                # Create the image entry with local URL
                image = UploadedImage.objects.create(file_name=file_name, file_url=file_url)

            else:
                # Upload the file to Backblaze B2 in production
                file_url, file_id = upload_file(file, file_name)
                
                # Create the image entry with the Backblaze URL and file ID
                image = UploadedImage.objects.create(file_name=file_name, file_url=file_url, file_id=file_id)

            # Pass the message to the success page
            return render(request, "app/success.html", {
                "message": "File uploaded successfully",
                "file_url": file_url
            })

    else:
        form = ImageUploadForm()

    return render(request, "app/upload.html", {"form": form})

def delete_image(request, image_id):
    image = get_object_or_404(UploadedImage, id=image_id)

    try:
        delete_file(image.file_id)
        image.delete()
        return JsonResponse({"message": "File deleted successfully"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def image_list(request):
    images = UploadedImage.objects.all()
    return render(request, "app/image_list.html", {"images": images})
