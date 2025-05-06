from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Doctor
from .serializers import DoctorSerializer
from rest_framework.permissions import IsAuthenticated

class DoctorListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer