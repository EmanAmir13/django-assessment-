from django.db import models

from api.models.project import Project


class Task(models.Model):
    STATUS_CHOICES = [
        ('to_do', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to_do')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
