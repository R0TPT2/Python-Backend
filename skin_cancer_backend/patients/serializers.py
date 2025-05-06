from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['gender'] = instance.get_gender_display()
        return representation