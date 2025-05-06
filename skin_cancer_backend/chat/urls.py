from django.urls import path
from . import views

urlpatterns = [
    path('messages/<uuid:ticket_id>/', views.ChatMessageListView.as_view(), name='chat-message-list'),
    path('messages/<uuid:ticket_id>/create/', views.ChatMessageCreateView.as_view(), name='chat-message-create'),
]