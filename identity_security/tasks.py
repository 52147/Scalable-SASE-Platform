from celery import shared_task
from .models import AccessLog, User

@shared_task
def log_access(user_id, resource_accessed, action):
    user = User.objects.get(id=user_id)
    AccessLog.objects.create(user=user, resource_accessed=resource_accessed, action=action)
