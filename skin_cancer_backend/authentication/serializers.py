from rest_framework import serializers
from patients.models import Patients
from doctors.models import Doctor
from django.contrib.auth.hashers import make_password


class PatientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Patients
        fields = ['national_id', 'name', 'email', 'password', 'phone', 'gender', 
                 'current_medical_conditions', 'allergies', 'past_surgeries', 
                 'family_medical_history', 'current_medications']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        patient = Patients.objects.create(
            password_hash=hashed_password,
            **validated_data
        )
        return patient


class PatientLoginSerializer(serializers.Serializer):
    national_id = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        national_id = data.get('national_id')
        password = data.get('password')
        
        if not national_id or not password:
            raise serializers.ValidationError("National ID and password are required.")
        
        return {
            'national_id': national_id,
            'password': password
        }

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['doctor_id', 'name', 'email', 'password_hash', 'specialty', 'clinic_location', 'operating_hours', 'education', 'experience']

    def create(self, validated_data):
        doctor = Doctor.objects.create(**validated_data)
        return doctor


class DoctorLoginSerializer(serializers.Serializer):
    doctor_id = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        doctor_id = data.get('doctor_id')
        password = data.get('password')
        
        if not doctor_id or not password:
            raise serializers.ValidationError("Doctor ID and password are required.")
            
        return {
            'doctor_id': doctor_id,
            'password': password
        }