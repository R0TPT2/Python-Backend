from django.urls import path
from . import views

urlpatterns = [
    path('patient/register/', views.PatientRegisterView.as_view(), name='patient-register'),
    path('patient/login/', views.PatientLoginView.as_view(), name='patient-login'),
    path('patient/profile/', views.PatientProfileView.as_view(), name='patient-profile'),
    path('doctor/login/', views.DoctorLoginView.as_view(), name='doctor-login'),
    path('doctor/profile/', views.DoctorProfileView.as_view(), name='doctor-profile'),
    path('token/', views.ObtainAuthToken.as_view(), name='api-token'),
]