from django.contrib import admin
from .models import User, AccessLog

admin.site.register(User)
admin.site.register(AccessLog)
