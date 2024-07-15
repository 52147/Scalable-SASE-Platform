from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework import routers
from identity_security.views import UserViewSet, AccessLogViewSet

# Define a simple view for the root URL
def home(request):
    return HttpResponse("Welcome to the SASE Platform")

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'access_logs', AccessLogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', home),  # Add this line to handle the root URL
]
