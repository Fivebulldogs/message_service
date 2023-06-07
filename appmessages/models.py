from django.db import models


class Message(models.Model):
    recipient = models.CharField(max_length=30)
    text = models.CharField(max_length=255)
    is_new = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
