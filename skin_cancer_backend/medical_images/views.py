from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MedicalImage
from .serializers import MedicalImageSerializer
from patients.models import Patients
from rest_framework.permissions import IsAuthenticated
import uuid
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
import os
from urllib.parse import urlparse
import logging

# Set up logger
logger = logging.getLogger(__name__)

class MedicalImageCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            # Log authentication information
            logger.info(f"User: {request.user}, Auth: {request.user.is_authenticated}")
            logger.info(f"Auth header: {request.META.get('HTTP_AUTHORIZATION', 'None')}")
            
            data = request.data.copy()
            
            patient_id = data.get('patient_id')
            if not patient_id:
                return Response({'error': 'Patient ID is required'},
                                status=status.HTTP_400_BAD_REQUEST)
                
            try:
                patient = Patients.objects.get(national_id=patient_id)
            except Patients.DoesNotExist:
                return Response({'error': f'Patient with National ID {patient_id} not found'},
                                status=status.HTTP_404_NOT_FOUND)
                
            image_path = data.get('image_path')
            if not image_path:
                return Response({'error': 'Image path is required'},
                                status=status.HTTP_400_BAD_REQUEST)
                
            lesion_type = data.get('lesion_type')
            if not lesion_type:
                return Response({'error': 'Lesion type is required'},
                                status=status.HTTP_400_BAD_REQUEST)
                
            diagnosis = data.get('diagnosis_result')
            if not diagnosis:
                primary_score = float(data.get('primary_ai_score', 0.0))
                diagnosis = 'MALIGNANT' if primary_score > 0.526 else 'BENIGN'
                
            medical_image = MedicalImage(
                id=uuid.uuid4(),
                patient=patient,
                image=image_path,
                diagnosis_result=diagnosis,
                primary_ai_score=float(data.get('primary_ai_score', 0.0)),
                secondary_ai_score=float(data.get('secondary_ai_score', 0.0)),
                lesion_type=lesion_type,
                priority=int(data.get('priority', 0)),
                doctor_notes=data.get('doctor_notes', '')
            )
            
            medical_image.save()
            
            serializer = MedicalImageSerializer(medical_image, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            logger.error(f"Error in MedicalImageCreateView: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, *args, **kwargs):
        logger.info(f"User: {request.user}, Auth: {request.user.is_authenticated}")
        logger.info(f"Auth header: {request.META.get('HTTP_AUTHORIZATION', 'None')}")
        logger.info(f"Request method: {request.method}")
        logger.info(f"Request FILES: {request.FILES.keys()}")
        
        if 'image' not in request.FILES:
            return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)
            
        image_file = request.FILES['image']
        filename = f"{uuid.uuid4()}{os.path.splitext(image_file.name)[1]}"
        
        filepath = os.path.join('images', filename)
        full_path = os.path.join(settings.MEDIA_ROOT, filepath)
        
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
                
        image_url = request.build_absolute_uri(settings.MEDIA_URL + filepath)
        logger.info(f"Image successfully saved at: {image_url}")
        return Response({'image_path': image_url}, status=status.HTTP_200_OK)