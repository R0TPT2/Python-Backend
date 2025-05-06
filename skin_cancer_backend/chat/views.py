from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from tickets.models import Ticket
from rest_framework.permissions import IsAuthenticated

class ChatMessageListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        ticket_id = self.kwargs['ticket_id']
        return ChatMessage.objects.filter(ticket_id=ticket_id).order_by('sent_at')

class ChatMessageCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer

    def perform_create(self, serializer):
        ticket_id = self.kwargs['ticket_id']
        serializer.save(ticket_id=ticket_id, sender_id=self.request.user.id)