from django.db import models
from medical_images.models import MedicalImage

class Ticket(models.Model):
    class TicketStatus(models.TextChoices):
        OPEN = 'OPEN'
        CLAIMED = 'CLAIMED'
        RESOLVED = 'RESOLVED'

    id = models.UUIDField(primary_key=True, editable=False)
    medical_image = models.ForeignKey(MedicalImage, on_delete=models.CASCADE, related_name='tickets')
    status = models.CharField(max_length=10, choices=TicketStatus.choices, default=TicketStatus.OPEN)
    claimed_by_doctor = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    claimed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Ticket {self.id} - Image {self.medical_image.id}"