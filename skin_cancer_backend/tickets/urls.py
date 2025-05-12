from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    # Ticket creation endpoint
    path('create/', views.create_ticket, name='create_ticket'),
    
    # Patient ticket endpoints
    path('patient/<str:patient_id>/', views.get_patient_tickets, name='get_patient_tickets'),
    
    # Individual ticket details
    path('<uuid:ticket_id>/', views.get_ticket_detail, name='get_ticket_detail'),
    
    # Ticket management endpoints for doctors
    path('<uuid:ticket_id>/claim/', views.claim_ticket, name='claim_ticket'),
    path('<uuid:ticket_id>/resolve/', views.resolve_ticket, name='resolve_ticket'),
    
    # Doctor-specific endpoints
    path('open/', views.get_open_tickets, name='get_open_tickets'),
    path('doctor/<str:doctor_id>/', views.get_doctor_tickets, name='get_doctor_tickets'),
]