from django.core.exceptions import ValidationError
from django.db import models

from api.models.user import User


class Project(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean(self):
        if self.creator.role != 'admin':
            raise ValidationError("Only admins can create projects.")
