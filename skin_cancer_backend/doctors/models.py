from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

class Doctor(models.Model):
    doctor_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    clinic_location = models.TextField(null=True, blank=True)
    operating_hours = models.TextField(null=True, blank=True)
    education = models.JSONField(default=list)
    experience = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name