from django.db import models
from medical_images.models import MedicalImage
import uuid
import json

class Ticket(models.Model):
    class TicketStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CLAIMED = 'claimed', 'Claimed'
        RESOLVED = 'resolved', 'Resolved'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_id = models.CharField(max_length=100,default='')
    medical_image = models.ForeignKey(MedicalImage, on_delete=models.CASCADE, related_name='tickets')
    symptom_data = models.JSONField(default=dict)
    diagnosis_result = models.CharField(max_length=20,default='')
    priority = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=TicketStatus.choices, default=TicketStatus.PENDING)
    claimed_by_doctor = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    claimed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Ticket {self.id} - Patient {self.patient_id}"
    
    def set_symptom_data(self, data_dict):
        self.symptom_data = json.dumps(data_dict)
    
    def get_symptom_data(self):
        if isinstance(self.symptom_data, str):
            return json.loads(self.symptom_data)
        return self.symptom_data