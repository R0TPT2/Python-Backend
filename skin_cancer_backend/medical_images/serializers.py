from rest_framework import serializers
from .models import MedicalImage

class MedicalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalImage
        fields = '__all__'
        read_only_fields = ['id', 'analyzed_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['diagnosis_result'] = instance.get_diagnosis_result_display()
        representation['priority'] = instance.get_priority_display()
        return representation