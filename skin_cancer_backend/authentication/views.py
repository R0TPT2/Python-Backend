from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Patient, Doctor
from .serializers import UserSerializer, PatientSerializer, DoctorSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if request.data.get('is_doctor'):
                doctor_serializer = DoctorSerializer(data=request.data)
                if doctor_serializer.is_valid():
                    doctor_serializer.save(user=user)
            else:
                patient_serializer = PatientSerializer(data=request.data)
                if patient_serializer.is_valid():
                    patient_serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

class PatientProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
            serializer = PatientSerializer(patient)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({'detail': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
            serializer = PatientSerializer(patient, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Patient.DoesNotExist:
            return Response({'detail': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

class DoctorProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            doctor = Doctor.objects.get(user=request.user)
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data)
        except Doctor.DoesNotExist:
            return Response({'detail': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            doctor = Doctor.objects.get(user=request.user)
            serializer = DoctorSerializer(doctor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Doctor.DoesNotExist:
            return Response({'detail': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)