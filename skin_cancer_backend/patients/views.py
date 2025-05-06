from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Patient
from .serializers import PatientSerializer
from rest_framework.permissions import IsAuthenticated

class PatientListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            patient = Patient.objects.get(user=request.user)
            serializer = PatientSerializer(patient)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({"detail": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        try:
            patient = Patient.objects.get(user=request.user)
            serializer = PatientSerializer(patient, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Patient.DoesNotExist:
            return Response({"detail": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)