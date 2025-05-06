from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('user/', views.UserDetailView.as_view(), name='user-detail'),
    path('patient/profile/', views.PatientProfileView.as_view(), name='patient-profile'),
    path('doctor/profile/', views.DoctorProfileView.as_view(), name='doctor-profile'),
]