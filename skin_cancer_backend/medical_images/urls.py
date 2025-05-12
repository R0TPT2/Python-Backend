from django.urls import path
from .views import MedicalImageCreateView, ImageUploadView

urlpatterns = [
    path('create/', MedicalImageCreateView.as_view(), name='medical-image-create'),
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
]