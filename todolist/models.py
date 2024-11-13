from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.


class Task(models.Model):
    PENDING = "pending"
    COMPLETED = "completed"
    STATUS_CHOICES = ((PENDING, "Pending"), (COMPLETED, "Completed"))

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    due_date = models.DateField(default=timezone.now, blank=True, null=True)
    created_at = models.DateField(default=timezone.now)
    completed_at = models.DateField(null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks"
    )

    def mark_as_completed(self):
        """Change task status to 'completed' and set completion date"""
        self.status = self.COMPLETED
        self.completed_at = timezone.now().date()
        self.save()
