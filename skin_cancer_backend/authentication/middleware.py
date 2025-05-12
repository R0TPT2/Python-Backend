from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt
from patients.models import Patients
from doctors.models import Doctor
import logging

logger = logging.getLogger(__name__)

class CustomJWTAuthentication(BaseAuthentication):
    """
    Custom JWT authentication for handling both patient and doctor authentication.
    """
    
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        
        if not auth_header:
            return None
            
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        else:
            token = auth_header
            
        try:
            payload = jwt.decode(
                token,
                settings.JWT_AUTH['SIGNING_KEY'],
                algorithms=[settings.JWT_AUTH['ALGORITHM']]
            )
            
            if payload.get('token_type') != 'access':
                raise AuthenticationFailed('Token is not an access token')
                
            user_id = payload.get('user_id')
            
            if not user_id:
                raise AuthenticationFailed('No user ID found in token')
                
            try:
                user = Patients.objects.get(national_id=user_id)
                return (user, token)
            except Patients.DoesNotExist:
                pass
                
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