from django.db import models
from django.contrib.auth.hashers import make_password, check_password
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

    @property
    def is_authenticated(self):
        return True

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return self.name