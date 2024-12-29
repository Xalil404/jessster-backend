from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    language = models.CharField(
        max_length=10,
        choices=[
            ('en', 'English'),
            ('ru', 'Russian'),
            ('ar', 'Arabic')
        ]
    )

    def __str__(self):
        return f"{self.name} ({self.language})"


class Post(models.Model):
    STATUS = ((0, "Draft"), (1, "Published"))
    LANGUAGES = (("en", "English"), ("ru", "Russian"), ("ar", "Arabic"))

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts")
    language = models.CharField(max_length=2, choices=LANGUAGES, default="en")
    number_of_views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
