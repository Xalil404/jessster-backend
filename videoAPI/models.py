from django.db import models
from cloudinary.models import CloudinaryField


class Video(models.Model):
    title = models.CharField(max_length=255)
    video = CloudinaryField('video', resource_type='video')  # Upload video to Cloudinary
    thumbnail = CloudinaryField('image')  # Thumbnail for the video
    description = models.TextField(blank=True)  # Optional description
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
