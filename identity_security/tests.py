from django.test import TestCase
from .models import User

class UserModelTest(TestCase):

    def setUp(self):
        User.objects.create(username="testuser", email="test@example.com", full_name="Test User", role="admin")

    def test_user_creation(self):
        user = User.objects.get(username="testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.full_name, "Test User")
        self.assertEqual(user.role, "admin")

    def test_user_str(self):
        user = User.objects.get(username="testuser")
        self.assertEqual(str(user), "testuser")
