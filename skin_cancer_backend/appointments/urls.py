from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AppointmentViewSet

# Create a router and register our viewset
router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')

# The API URLs are determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]

# This will generate the following URL patterns:
# - /appointments/ - GET (list), POST (create)
# - /appointments/{id}/ - GET (retrieve), PUT (update), PATCH (partial_update), DELETE (destroy)
# - /appointments/today/ - GET (custom action for today's appointments)
# - /appointments/by_doctor/ - GET (custom action for doctor's appointments)
# - /appointments/by_patient/ - GET (custom action for patient's appointments)
# - /appointments/{id}/confirm/ - POST (custom action to confirm an appointment)
# - /appointments/{id}/cancel/ - POST (custom action to cancel an appointment)