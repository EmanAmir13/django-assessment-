from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('member', 'Member'),
]


class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField('email address', unique=True, blank=False, null=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    def __str__(self):
        return self.email
