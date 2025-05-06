from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.PatientCreateView.as_view(), name='patient-create'),
    path('list/', views.PatientListView.as_view(), name='patient-list'),
    path('detail/<str:national_id>/', views.PatientDetailView.as_view(), name='patient-detail'),
    path('update/<str:national_id>/', views.PatientUpdateView.as_view(), name='patient-update'),
    path('delete/<str:national_id>/', views.PatientDeleteView.as_view(), name='patient-delete'),
    path('profile/', views.PatientProfileView.as_view(), name='patient-profile'),
]