from datetime import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Ticket
from .serializers import TicketSerializer
from medical_images.models import MedicalImage
from rest_framework.permissions import IsAuthenticated

class TicketListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketClaimView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response({"detail": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)
        
        ticket.status = 'CLAIMED'
        ticket.claimed_by_doctor = request.user.username
        ticket.claimed_at = timezone.now()
        ticket.save()
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

class TicketResolveView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response({"detail": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)
        
        ticket.status = 'RESOLVED'
        ticket.save()
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)