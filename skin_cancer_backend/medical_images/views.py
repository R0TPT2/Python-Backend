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

class MedicalImageCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
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
            
            image_url = data.get('image_path')
            if not image_url:
                return Response({'error': 'Image path is required'}, 
                               status=status.HTTP_400_BAD_REQUEST)
                
            from urllib.parse import urlparse
            parsed_url = urlparse(image_url)
            path = parsed_url.path
            
            media_prefix = settings.MEDIA_URL.strip('/')
            if media_prefix and path.startswith(f"/{media_prefix}/"):
                path = path[len(f"/{media_prefix}/"):]
            elif path.startswith('/'):
                path = path[1:]
                
            diagnosis = data.get('diagnosis_result')
            if not diagnosis:
                primary_score = float(data.get('primary_ai_score', 0.0))
                diagnosis = 'MALIGNANT' if primary_score > 0.5 else 'BENIGN'
                
            medical_image = MedicalImage(
                id=uuid.uuid4(),
                patient=patient,
                image=path,
                diagnosis_result=diagnosis,
                primary_ai_score=float(data.get('primary_ai_score', 0.0)),
                secondary_ai_score=float(data.get('secondary_ai_score', 0.0)),
                lesion_type=data.get('lesion_type', ''),
                priority=int(data.get('priority', 0)),
                doctor_notes=data.get('doctor_notes', '')
            )
            
            medical_image.save()
            
            serializer = MedicalImageSerializer(medical_image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            import traceback
            return Response({
                'error': str(e),
                'traceback': traceback.format_exc()
            }, status=status.HTTP_400_BAD_REQUEST)
        
class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, *args, **kwargs):
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
        return Response({'image_path': image_url}, status=status.HTTP_201_CREATED)
    
class MedicalImageListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MedicalImage.objects.all()
    serializer_class = MedicalImageSerializer

class MedicalImageDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MedicalImage.objects.all()
    serializer_class = MedicalImageSerializer

class MedicalImageUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MedicalImage.objects.all()
    serializer_class = MedicalImageSerializer

class MedicalImageDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MedicalImage.objects.all()
    serializer_class = MedicalImageSerializer