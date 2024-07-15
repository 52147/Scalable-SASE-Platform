from rest_framework import viewsets
from .models import User, AccessLog
from .serializers import UserSerializer, AccessLogSerializer
from .tasks import log_access
from django.http import HttpResponse

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        log_access.delay(user.id, 'user_created', 'create')

class AccessLogViewSet(viewsets.ModelViewSet):
    queryset = AccessLog.objects.all()
    serializer_class = AccessLogSerializer

def home(request):
    return HttpResponse("Welcome to the SASE Platform")
