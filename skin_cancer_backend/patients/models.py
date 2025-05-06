from django.db import models
from django.contrib.postgres.fields import ArrayField

class Patient(models.Model):
    national_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10)
    current_medical_conditions = ArrayField(models.CharField(max_length=255), default=list)
    allergies = ArrayField(models.CharField(max_length=255), default=list)
    past_surgeries = ArrayField(models.CharField(max_length=255), default=list)
    family_medical_history = ArrayField(models.CharField(max_length=255), default=list)
    current_medications = ArrayField(models.CharField(max_length=255), default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name