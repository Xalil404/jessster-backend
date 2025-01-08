from django.db import models
from cloudinary.models import CloudinaryField


class Video(models.Model):
    STATUS = ((0, "Draft"), (1, "Published"))
    LANGUAGES = [
        ('en', 'English'),
        ('ru', 'Russian'),
        ('ar', 'Arabic'),
    ]
    
    title = models.CharField(max_length=255)
    video = CloudinaryField('video', resource_type='video')  # Upload video to Cloudinary (required)
    description = models.TextField(blank=True)  # Optional description
    created_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=2, choices=LANGUAGES, default='en')  # Language selector
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.title
