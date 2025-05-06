from rest_framework import serializers
from .models import Ticket
from medical_images.models import MedicalImage

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'claimed_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = instance.get_status_display()
        representation['medical_image_id'] = str(instance.medical_image.id)
        return representation