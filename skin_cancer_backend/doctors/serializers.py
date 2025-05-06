from rest_framework import serializers
from .models import Doctor
from authentication.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['specialty'] = instance.specialty
        representation['clinic_location'] = instance.clinic_location
        representation['operating_hours'] = instance.operating_hours
        return representation