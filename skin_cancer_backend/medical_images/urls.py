from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.MedicalImageCreateView.as_view(), name='medical-image-create'),
    path('list/', views.MedicalImageListView.as_view(), name='medical-image-list'),
    path('detail/<uuid:pk>/', views.MedicalImageDetailView.as_view(), name='medical-image-detail'),
    path('update/<uuid:pk>/', views.MedicalImageUpdateView.as_view(), name='medical-image-update'),
    path('delete/<uuid:pk>/', views.MedicalImageDeleteView.as_view(), name='medical-image-delete'),
    path('upload/', views.MedicalImageCreateView.as_view(), name='medical-image-upload')
]