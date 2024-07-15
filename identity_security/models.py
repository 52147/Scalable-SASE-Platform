from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_time = models.DateTimeField(auto_now_add=True, db_index=True)
    resource_accessed = models.CharField(max_length=100)
    action = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user.username} accessed {self.resource_accessed} at {self.access_time}'
