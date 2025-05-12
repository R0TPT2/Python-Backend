from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Ticket
from medical_images.models import MedicalImage
from .serializers import TicketSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_ticket(request):
    """
    Create a new ticket with medical image ID and symptom data
    """
    data = request.data
    
    # Check required fields
    required_fields = ['patient_id', 'medical_image_id', 'diagnosis_result', 'priority']
    for field in required_fields:
        if field not in data:
            return Response(
                {"error": f"Missing required field: {field}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    try:
        # Get the medical image
        medical_image = get_object_or_404(MedicalImage, id=data['medical_image_id'])
        
        # Create the ticket
        ticket = Ticket(
            patient_id=data['patient_id'],
            medical_image=medical_image,
            diagnosis_result=data['diagnosis_result'],
            priority=data['priority'],
            status=data.get('status', 'pending'),
            symptom_data=data.get('symptom_data', {})
        )
        ticket.save()
        
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient_tickets(request, patient_id):
    """
    Get all tickets for a specific patient
    """
    tickets = Ticket.objects.filter(patient_id=patient_id).order_by('-created_at')
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ticket_detail(request, ticket_id):
    """
    Get detailed information about a specific ticket
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    serializer = TicketSerializer(ticket)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def claim_ticket(request, ticket_id):
    """
    Allow a doctor to claim a ticket for review
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    

    if ticket.status == Ticket.TicketStatus.CLAIMED and ticket.claimed_by_doctor != request.data.get('doctor_id'):
        return Response(
            {"error": "This ticket is already claimed by another doctor"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    ticket.status = Ticket.TicketStatus.CLAIMED
    ticket.claimed_by_doctor = request.data.get('doctor_id')
    ticket.claimed_at = timezone.now()
    ticket.save()
    
    serializer = TicketSerializer(ticket)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def resolve_ticket(request, ticket_id):
    """
    Mark a ticket as resolved with doctor's feedback
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Make sure the ticket is claimed by this doctor
    if ticket.claimed_by_doctor != request.data.get('doctor_id'):
        return Response(
            {"error": "Only the doctor who claimed this ticket can resolve it"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    ticket.status = Ticket.TicketStatus.RESOLVED
    
    # If there's doctor feedback, save it to the medical image
    if 'doctor_feedback' in request.data:
        medical_image = ticket.medical_image
        medical_image.doctor_feedback = request.data['doctor_feedback']
        medical_image.save()
    
    ticket.save()
    
    serializer = TicketSerializer(ticket)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_open_tickets(request):
    """
    Get all open tickets for doctors to claim
    """
    tickets = Ticket.objects.filter(status=Ticket.TicketStatus.PENDING).order_by('-priority', '-created_at')
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctor_tickets(request, doctor_id):
    """
    Get all tickets claimed by a specific doctor
    """
    tickets = Ticket.objects.filter(claimed_by_doctor=doctor_id).order_by('-created_at')
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)