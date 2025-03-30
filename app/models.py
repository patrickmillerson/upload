from django.db import models

class UploadedImage(models.Model):
    file_name = models.CharField(max_length=255)
    file_url = models.URLField()
    file_id = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
