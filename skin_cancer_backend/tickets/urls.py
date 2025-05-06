from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.TicketListView.as_view(), name='ticket-list'),
    path('create/', views.TicketCreateView.as_view(), name='ticket-create'),
    path('detail/<uuid:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('update/<uuid:pk>/', views.TicketUpdateView.as_view(), name='ticket-update'),
    path('delete/<uuid:pk>/', views.TicketDeleteView.as_view(), name='ticket-delete'),
    path('claim/<uuid:pk>/', views.TicketClaimView.as_view(), name='ticket-claim'),
    path('resolve/<uuid:pk>/', views.TicketResolveView.as_view(), name='ticket-resolve'),
]