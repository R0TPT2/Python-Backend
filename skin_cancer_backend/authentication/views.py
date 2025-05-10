from rest_framework import generics, status
import jwt
import datetime
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from patients.models import Patients
from doctors.models import Doctor
from .serializers import PatientSerializer, DoctorSerializer, PatientLoginSerializer, DoctorLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

class PatientRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PatientLoginSerializer(data=request.data)
        if serializer.is_valid():
            national_id = serializer.validated_data['national_id']
            password = serializer.validated_data['password']
            
            try:
                patient = Patients.objects.get(national_id=national_id)
                
                if check_password(password, patient.password_hash):
                    access_payload = {
                        'user_id': patient.national_id,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                        'iat': datetime.datetime.utcnow(),
                        'token_type': 'access'
                    }
                    
                    refresh_payload = {
                        'user_id': patient.national_id,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=14),
                        'iat': datetime.datetime.utcnow(),
                        'token_type': 'refresh'
                    }
                    
                    access_token = jwt.encode(
                        access_payload,
                        api_settings.SIGNING_KEY,
                        algorithm=api_settings.ALGORITHM
                    )
                    
                    refresh_token = jwt.encode(
                        refresh_payload,
                        api_settings.SIGNING_KEY,
                        algorithm=api_settings.ALGORITHM
                    )
                    
                    return Response({
                        'refresh': refresh_token,
                        'access': access_token,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'detail': 'Invalid credentials'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            except Patients.DoesNotExist:
                return Response(
                    {'detail': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            patient = Patients.objects.get(email=request.user.email)
            serializer = PatientSerializer(patient)
            return Response(serializer.data)
        except Patients.DoesNotExist:
            return Response({'detail': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            patient = Patients.objects.get(email=request.user.email)
            serializer = PatientSerializer(patient, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Patients.DoesNotExist:
            return Response({'detail': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

class DoctorLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = DoctorLoginSerializer(data=request.data)
        if serializer.is_valid():
            doctor_id = serializer.validated_data['doctor_id']
            password = serializer.validated_data['password']
            
            try:
                doctor = Doctor.objects.get(doctor_id=doctor_id)
                
                if check_password(password, doctor.password_hash):
                    access_payload = {
                        'user_id': doctor.doctor_id,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                        'iat': datetime.datetime.utcnow(),
                        'token_type': 'access'
                    }
                    
                    refresh_payload = {
                        'user_id': doctor.doctor_id,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=14),
                        'iat': datetime.datetime.utcnow(),
                        'token_type': 'refresh'
                    }
                    
                    access_token = jwt.encode(
                        access_payload,
                        api_settings.SIGNING_KEY,
                        algorithm=api_settings.ALGORITHM
                    )
                    
                    refresh_token = jwt.encode(
                        refresh_payload,
                        api_settings.SIGNING_KEY,
                        algorithm=api_settings.ALGORITHM
                    )
                    
                    return Response({
                        'refresh': refresh_token,
                        'access': access_token,
                        'name': doctor.name  # Include doctor's name for the frontend
                    }, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'detail': 'Invalid credentials'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            except Doctor.DoesNotExist:
                return Response(
                    {'detail': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            doctor = Doctor.objects.get(email=request.user.email)
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data)
        except Doctor.DoesNotExist:
            return Response({'detail': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            doctor = Doctor.objects.get(email=request.user.email)
            serializer = DoctorSerializer(doctor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Doctor.DoesNotExist:
            return Response({'detail': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)