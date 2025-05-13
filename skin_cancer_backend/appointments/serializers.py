from rest_framework import serializers
from .models import Appointment, Patients, Doctor

class DoctorMinSerializer(serializers.ModelSerializer):
    """Minimal doctor information for appointment lists"""
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization']

class PatientMinSerializer(serializers.ModelSerializer):
    """Minimal patient information for appointment lists"""
    class Meta:
        model = Patients
        fields = ['id', 'name', 'phone_number']

class AppointmentSerializer(serializers.ModelSerializer):
    """Full appointment serializer with nested patient and doctor data"""
    patient_details = PatientMinSerializer(source='patient', read_only=True)
    doctor_details = DoctorMinSerializer(source='doctor', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'doctor', 'clinic_location', 
            'scheduled_time', 'status', 'created_at',
            'patient_details', 'doctor_details', 'status_display'
        ]
        read_only_fields = ['id', 'created_at']

class AppointmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating appointments"""
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'clinic_location', 'scheduled_time', 'status']
    
    def validate_scheduled_time(self, value):
        """Validate that appointment time is in the future"""
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError("Appointment time must be in the future.")
        return value