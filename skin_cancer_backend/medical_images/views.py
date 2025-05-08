from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MedicalImage
from .serializers import MedicalImageSerializer
from patients.models import Patients
from rest_framework.permissions import IsAuthenticated


class MedicalImageCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = MedicalImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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