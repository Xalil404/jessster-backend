from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # To handle active or unsubscribed status

    def __str__(self):
        return self.email
