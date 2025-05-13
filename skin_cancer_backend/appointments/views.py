from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q

from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentCreateSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing appointments
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'doctor', 'patient']
    search_fields = ['patient__name', 'doctor__name', 'clinic_location']
    ordering_fields = ['scheduled_time', 'created_at', 'status']
    ordering = ['-scheduled_time']

    def get_queryset(self):
        """
        Get appointments with optional filtering
        """
        queryset = Appointment.objects.all()
        
        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(scheduled_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(scheduled_time__lte=end_date)
            
        # Filter for upcoming appointments
        upcoming = self.request.query_params.get('upcoming')
        if upcoming and upcoming.lower() == 'true':
            queryset = queryset.filter(scheduled_time__gte=timezone.now())
            
        return queryset

    def get_serializer_class(self):
        """
        Use different serializers for list/retrieve vs create/update
        """
        if self.action in ['create', 'update', 'partial_update']:
            return AppointmentCreateSerializer
        return AppointmentSerializer
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """
        Get all appointments scheduled for today
        """
        today = timezone.now().date()
        appointments = Appointment.objects.filter(
            scheduled_time__date=today
        ).order_by('scheduled_time')
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_doctor(self, request):
        """
        Get appointments for a specific doctor
        """
        doctor_id = request.query_params.get('doctor_id')
        if not doctor_id:
            return Response(
                {"error": "doctor_id parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        appointments = Appointment.objects.filter(doctor_id=doctor_id)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        """
        Get appointments for a specific patient
        """
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response(
                {"error": "patient_id parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        appointments = Appointment.objects.filter(patient_id=patient_id)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """
        Confirm an appointment
        """
        appointment = self.get_object()
        appointment.status = Appointment.AppointmentStatus.CONFIRMED
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel an appointment
        """
        appointment = self.get_object()
        appointment.status = Appointment.AppointmentStatus.CANCELLED
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)