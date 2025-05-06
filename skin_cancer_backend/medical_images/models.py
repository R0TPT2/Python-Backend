from django.db import models
from patients.models import Patient
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator

class MedicalImage(models.Model):
    class DiagnosisResult(models.TextChoices):
        BENIGN = 'BENIGN'
        MALIGNANT = 'MALIGNANT'

    class Priority(models.IntegerChoices):
        LOW = 0
        MEDIUM = 1
        HIGH = 2

    id = models.UUIDField(primary_key=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_images')
    image = models.ImageField(upload_to='images/')
    diagnosis_result = models.CharField(max_length=10, choices=DiagnosisResult.choices)
    primary_ai_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    secondary_ai_score = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    lesion_type = models.CharField(max_length=30)
    priority = models.IntegerField(choices=Priority.choices)
    doctor_notes = models.TextField(null=True, blank=True)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} - Patient {self.patient.national_id}"