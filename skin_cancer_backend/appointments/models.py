from django.db import models
from django.contrib.postgres.fields import ArrayField
from patients.models import Patients
from doctors.models import Doctor

class Appointment(models.Model):
    class AppointmentStatus(models.TextChoices):
        PENDING = 'PENDING'
        CONFIRMED = 'CONFIRMED'
        CANCELLED = 'CANCELLED'

    id = models.UUIDField(primary_key=True, editable=False)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    clinic_location = models.TextField(null=True, blank=True)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=AppointmentStatus.choices, default=AppointmentStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment {self.id} - {self.patient.name} - {self.scheduled_time}"