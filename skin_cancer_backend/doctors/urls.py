from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.DoctorListView.as_view(), name='doctor-list'),
    path('create/', views.DoctorCreateView.as_view(), name='doctor-create'),
    path('detail/<uuid:pk>/', views.DoctorDetailView.as_view(), name='doctor-detail'),
    path('update/<uuid:pk>/', views.DoctorUpdateView.as_view(), name='doctor-update'),
    path('delete/<uuid:pk>/', views.DoctorDeleteView.as_view(), name='doctor-delete'),
]