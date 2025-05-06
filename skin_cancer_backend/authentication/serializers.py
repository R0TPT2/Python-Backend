from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Patient, Doctor

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'is_staff']
        read_only_fields = ['is_active', 'is_staff']

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = ['user', 'national_id', 'name', 'phone', 'gender', 'current_medical_conditions', 'allergies', 'past_surgeries', 'family_medical_history', 'current_medications']

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = ['user', 'doctor_id', 'name', 'specialty', 'clinic_location', 'operating_hours', 'education', 'experience']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return data