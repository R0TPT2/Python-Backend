from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Appointment
from .serializers import AppointmentSerializer
from patients.models import Patients
from doctors.models import Doctor
from rest_framework.permissions import IsAuthenticated

class AppointmentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AppointmentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({"message": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        appointment.status = 'CONFIRMED'
        appointment.save()
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

class AppointmentCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({"message": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        appointment.status = 'CANCELLED'
        appointment.save()
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)