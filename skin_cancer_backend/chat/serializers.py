from rest_framework import serializers
from .models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'
        read_only_fields = ['id', 'sent_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ticket_id'] = str(instance.ticket.id)
        return representation