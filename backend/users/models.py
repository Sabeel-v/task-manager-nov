from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'SuperAdmin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    assigned_admin = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_users', limit_choices_to={'role': 'admin'})