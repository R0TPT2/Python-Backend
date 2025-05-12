from rest_framework import serializers
from .models import Ticket
from medical_images.serializers import MedicalImageSerializer

class TicketSerializer(serializers.ModelSerializer):
    medical_image_details = MedicalImageSerializer(source='medical_image', read_only=True)
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'patient_id', 'medical_image', 'medical_image_details',
            'symptom_data', 'diagnosis_result', 'priority',
            'status', 'claimed_by_doctor', 'created_at', 'claimed_at'
        ]
        read_only_fields = ['id', 'created_at', 'claimed_at']