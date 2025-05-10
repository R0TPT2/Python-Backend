from rest_framework import serializers
from .models import MedicalImage
from rest_framework import serializers
from .models import MedicalImage
from patients.models import Patients

class MedicalImageSerializer(serializers.ModelSerializer):
    # Add a field for patient_id (national_id)
    patient_id = serializers.CharField(source='patient.national_id', read_only=True)
    
    class Meta:
        model = MedicalImage
        fields = ['id', 'patient', 'patient_id', 'image', 'diagnosis_result', 
                 'primary_ai_score', 'secondary_ai_score', 'lesion_type', 
                 'priority', 'doctor_notes', 'analyzed_at']
        read_only_fields = ['id', 'analyzed_at']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['patient_name'] = instance.patient.name
        representation['diagnosis_result'] = instance.get_diagnosis_result_display()
        representation['priority'] = instance.get_priority_display()
        
        request = self.context.get('request')
        if request and instance.image:
            representation['image_url'] = request.build_absolute_uri(instance.image.url)
            
        return representation