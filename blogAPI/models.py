from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=50)
    language = models.CharField(
        max_length=10,
        choices=[('en', 'English'), ('ru', 'Russian'), ('ar', 'Arabic')]
    )
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Automatically generate a slug from the name and language
            self.slug = slugify(f"{self.name}-{self.language}")
        
        # Ensure the slug is unique by checking against other categories with the same language
        count = Category.objects.filter(slug=self.slug, language=self.language).count()
        if count > 0:
            self.slug = f"{self.slug}-{count+1}"
        
        super().save(*args, **kwargs)

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
    comment_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def increment_views(self):
        self.number_of_views += 1
        self.save() 

    def update_comment_count(self):
        """Manually update the comment count."""
        self.comment_count = self.comments.count()
        self.save()



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
