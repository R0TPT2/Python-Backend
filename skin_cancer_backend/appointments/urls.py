from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.AppointmentCreateView.as_view(), name='appointment-create'),
    path('list/', views.AppointmentListView.as_view(), name='appointment-list'),
    path('detail/<uuid:pk>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('update/<uuid:pk>/', views.AppointmentUpdateView.as_view(), name='appointment-update'),
    path('delete/<uuid:pk>/', views.AppointmentDeleteView.as_view(), name='appointment-delete'),
    path('confirm/<uuid:pk>/', views.AppointmentConfirmView.as_view(), name='appointment-confirm'),
    path('cancel/<uuid:pk>/', views.AppointmentCancelView.as_view(), name='appointment-cancel'),
]