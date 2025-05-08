from rest_framework import serializers
from .models import Patients

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = '__all__'
        read_only_fields = ['created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['gender'] = instance.get_gender_display()
        return representation