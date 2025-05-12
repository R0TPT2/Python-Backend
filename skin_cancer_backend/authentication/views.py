from rest_framework import generics, status
import jwt
import datetime
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from patients.models import Patients
from doctors.models import Doctor
from .serializers import PatientSerializer, DoctorSerializer, PatientLoginSerializer, DoctorLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.conf import settings
import logging
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class PatientRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthToken(APIView):
    permission_classes = []  
    
    def post(self, request):
        username = request.data.get('name')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    
class PatientLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PatientLoginSerializer(data=request.data)
        if serializer.is_valid():
            national_id = serializer.validated_data['national_id']
            password = serializer.validated_data['password']
            
            try:
                patient = Patients.objects.get(national_id=national_id)
                
                if check_password(password, patient.password_hash):
                    access_payload = {
                        'user_id': patient.national_id,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_AUTH['ACCESS_TOKEN_LIFETIME']),
                        'iat': datetime.datetime.utcnow(),
                        'token_type': 'access'
                    }
                    
                    refresh_payload = {
                        'user_id': patient.national_id,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_AUTH['REFRESH_TOKEN_LIFETIME']),
                        'iat': datetime.datetime.utcnow(),
                        'token_type': 'refresh'
                    }
                    
                    access_token = jwt.encode(
                        access_payload,
                        settings.JWT_AUTH['SIGNING_KEY'],
                        algorithm=settings.JWT_AUTH['ALGORITHM']
                    )
                    
                    refresh_token = jwt.encode(
                        refresh_payload,
                        settings.JWT_AUTH['SIGNING_KEY'],
                        algorithm=settings.JWT_AUTH['ALGORITHM']
                    )
                    
                    return Response({
                        'refresh': refresh_token,
                        'access': access_token,
                        'user_id': patient.national_id,
                        'name': patient.name
                    }, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'detail': 'Invalid credentials'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            except Patients.DoesNotExist:
                return Response(
                    {'detail': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not isinstance(request.user, Patients):
            return Response({'detail': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = PatientSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        if not isinstance(request.user, Patients):
            return Response({'detail': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = PatientSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = DoctorLoginSerializer(data=request.data)
        if serializer.is_valid():
            doctor_id = serializer.validated_data['doctor_id']
            password = serializer.validated_data['password']
        
            try:
                doctor = Doctor.objects.get(doctor_id=doctor_id)
            
                if check_password(password, doctor.password_hash):
                    access_payload = {
                        'user_id': doctor.doctor_id,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                        'iat': datetime.datetime.utcnow(),
                        'token_type': 'access'
                    }
                
                    refresh_payload = {
                        'user_id': doctor.doctor_id,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=14),
                        'iat': datetime.datetime.utcnow(),
                        'token_type': 'refresh'
                    }
                
                    access_token = jwt.encode(
                        access_payload,
                        api_settings.SIGNING_KEY,
                        algorithm=api_settings.ALGORITHM
                    )
                
                    refresh_token = jwt.encode(
                        refresh_payload,
                        api_settings.SIGNING_KEY,
                        algorithm=api_settings.ALGORITHM
                    )
                
                    return Response({
                        'refresh': refresh_token,
                        'access': access_token,
                        'user_id': doctor.doctor_id,
                        'name': doctor.name
                    }, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'detail': 'Invalid credentials'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            except Doctor.DoesNotExist:
                return Response(
                    {'detail': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DoctorProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            doctor = Doctor.objects.get(email=request.user.email)
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data)
        except Doctor.DoesNotExist:
            return Response({'detail': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            doctor = Doctor.objects.get(email=request.user.email)
            serializer = DoctorSerializer(doctor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Doctor.DoesNotExist:
            return Response({'detail': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        

# Set up logger
logger = logging.getLogger(__name__)

class JWTAuthenticationTestView(APIView):
    """
    A view to test if JWT authentication is working correctly.
    This is useful for debugging authentication issues.
    """
    
    def get(self, request, *args, **kwargs):
        # Get the auth header
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        
        logger.info(f"Auth test - Raw auth header: {auth_header}")
        
        if not auth_header:
            return Response({
                'error': 'Authorization header is missing',
                'status': 'failed'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Try to validate the token manually
        try:
            # For JWT tokens without Bearer prefix
            token = auth_header
            
            # Try with Bearer prefix removal if it exists
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
                
            logger.info(f"Auth test - Attempting to decode token: {token[:10]}...")
            
            # Try to decode the JWT token - Use JWT_AUTH instead of SIMPLE_JWT
            payload = jwt.decode(
                token,
                settings.JWT_AUTH['SIGNING_KEY'],
                algorithms=[settings.JWT_AUTH['ALGORITHM']]
            )
            
            logger.info(f"Auth test - Token decoded successfully: {payload}")
            
            return Response({
                'message': 'Authentication successful',
                'user_id': payload.get('user_id'),
                'token_type': payload.get('token_type'),
                'status': 'success'
            }, status=status.HTTP_200_OK)
            
        except jwt.ExpiredSignatureError:
            logger.error("Auth test - Token has expired")
            return Response({
                'error': 'Token has expired',
                'status': 'failed'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        except jwt.InvalidTokenError as e:
            logger.error(f"Auth test - Invalid token: {str(e)}")
            return Response({
                'error': f'Invalid token: {str(e)}',
                'status': 'failed'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        except Exception as e:
            logger.error(f"Auth test - Error validating token: {str(e)}")
            return Response({
                'error': f'Error validating token: {str(e)}',
                'status': 'failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomAuthMiddlewareTestView(APIView):
    """
    A view protected by the default DRF IsAuthenticated permission.
    This checks if the authentication classes are working properly.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        logger.info(f"Custom middleware test - User: {request.user}")
        logger.info(f"Custom middleware test - Is authenticated: {request.user.is_authenticated}")
        
        return Response({
            'message': 'You are authenticated',
            'user': str(request.user),
            'auth_method': str(request.auth),
            'status': 'success'
        }, status=status.HTTP_200_OK)
    

class CustomJWTAuthentication(BaseAuthentication):
    """
    Custom JWT authentication for handling both patient and doctor authentication.
    """
    
    def authenticate(self, request):
        # Get the auth header
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        
        if not auth_header:
            return None
            
        # Handle 'Bearer' prefix if present
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        else:
            token = auth_header
            
        try:
            # Decode the JWT token
            payload = jwt.decode(
                token,
                settings.JWT_AUTH['SIGNING_KEY'],
                algorithms=[settings.JWT_AUTH['ALGORITHM']]
            )
            
            # Check token type
            if payload.get('token_type') != 'access':
                raise AuthenticationFailed('Token is not an access token')
                
            user_id = payload.get('user_id')
            
            if not user_id:
                raise AuthenticationFailed('No user ID found in token')
                
            # Try to get user based on the token contents
            # First try as a patient
            try:
                user = Patients.objects.get(national_id=user_id)
                return (user, token)
            except Patients.DoesNotExist:
                pass
                
            # Then try as a doctor
            try:
                user = Doctor.objects.get(doctor_id=user_id)
                return (user, token)
            except Doctor.DoesNotExist:
                raise AuthenticationFailed('User not found')
                
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
            
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token: {str(e)}")
            raise AuthenticationFailed(f'Invalid token: {str(e)}')
            
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise AuthenticationFailed(f'Authentication error: {str(e)}')
            
        return None