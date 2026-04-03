from django.db import models
from django.conf import settings

class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    completion_report = models.TextField(blank=True, null=True)
    worked_hours = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title

    
    def save(self, *args, **kwargs):
        if self.status == 'completed':
            if not self.completion_report or not self.worked_hours:
                raise ValueError("Completion report and worked hours are required")
        super().save(*args, **kwargs)