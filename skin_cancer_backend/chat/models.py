from django.db import models
from tickets.models import Ticket

class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    sender_id = models.CharField(max_length=20)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} - Ticket {self.ticket.id}"