from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Comment, Post

@receiver(post_save, sender=Comment)
def update_comment_count_on_add(sender, instance, **kwargs):
    """Update comment count when a new comment is added."""
    post = instance.post
    post.comment_count = post.comments.count()
    post.save()

@receiver(post_delete, sender=Comment)
def update_comment_count_on_delete(sender, instance, **kwargs):
    """Update comment count when a comment is deleted."""
    post = instance.post
    post.comment_count = post.comments.count()
    post.save()
