from rest_framework import serializers
from .models import Appointment
from patients.models import Patient
from doctors.models import Doctor

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['national_id', 'name', 'email']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['doctor_id', 'name', 'email', 'specialty']

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = instance.get_status_display()
        return representation