from django.db import models
from django.conf import settings


# Create your models here.
class Feedback(models.Model):
    writer = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="feedbacks",
    )
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return f"{self.writer.username}"

    class Meta:
        indexes = [
            models.Index(
                fields=["created_at"],
            )
        ]
        ordering = ["-created_at"]
