from django.urls import path
from .views import upload_image, delete_image, image_list

urlpatterns = [
    path("upload/", upload_image, name="upload_image"),
    path("delete/<int:image_id>/", delete_image, name="delete_image"),
    path("", image_list, name="image_list"),
]