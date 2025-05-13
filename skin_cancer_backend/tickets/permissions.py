from rest_framework import permissions
import logging

logger = logging.getLogger(__name__)

class IsPatientOwnerOrDoctor(permissions.BasePermission):
    """
    Custom permission to only allow:
    - The patient who owns the data to access it
    - A doctor to access any patient data
    - An admin to access any patient data
    """
    
    def has_permission(self, request, view):
        # Get the patient_id from the URL parameter
        patient_id = view.kwargs.get('patient_id')
        
        # Log authentication details for debugging
        logger.debug(f"Auth check for patient_id: {patient_id}")
        logger.debug(f"User: {request.user}, Auth: {request.user.is_authenticated}")
        logger.debug(f"User type: {type(request.user)}")
        
        if hasattr(request.user, 'patient'):
            logger.debug(f"User patient: {request.user.patient}")
        
        if hasattr(request.user, 'is_doctor'):
            logger.debug(f"Is doctor: {request.user.is_doctor}")
            
        # User must be authenticated
        if not request.user.is_authenticated:
            logger.debug("Permission denied: User not authenticated")
            return False
            
        # Check if the user is an admin or staff
        if request.user.is_staff or request.user.is_superuser:
            logger.debug("Permission granted: User is admin/staff")
            return True
            
        # Check if the user is a doctor (adjust these checks based on your user model)
        if hasattr(request.user, 'is_doctor') and request.user.is_doctor:
            logger.debug("Permission granted: User is doctor")
            return True
            
        # Check if the user's national_id matches the patient_id in the URL
        # This handles the case for patient users
        if hasattr(request.user, 'national_id') and request.user.national_id == patient_id:
            logger.debug("Permission granted: User's national_id matches patient_id")
            return True
            
        # Check if the patient_id matches what's stored in the user's profile
        if hasattr(request.user, 'patient') and hasattr(request.user.patient, 'national_id') and request.user.patient.national_id == patient_id:
            logger.debug("Permission granted: User's patient profile matches patient_id")
            return True
            
        # If we include patient_id in JWT token claims, check auth token claims
        # This is for handling mobile app users via JWT
        if hasattr(request, 'auth') and hasattr(request.auth, 'payload'):
            token_patient_id = request.auth.payload.get('patient_id')
            logger.debug(f"Token patient_id: {token_patient_id}")
            if token_patient_id == patient_id:
                logger.debug("Permission granted: JWT token patient_id matches")
                return True
                
        logger.debug("Permission denied: No matching criteria")
        return False