from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserModelTest(TestCase):
    def test_user_creation_with_role(self):
        # Test creating a user with customer role
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role=User.Roles.CUSTOMER,
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.role, User.Roles.CUSTOMER)
        self.assertTrue(user.check_password("testpass123"))

    def test_user_creation_merchant_role(self):
        # Test creating a user with merchant role
        user = User.objects.create_user(
            username="merchantuser",
            email="merchant@example.com",
            password="testpass123",
            role=User.Roles.MERCHANT,
        )
        self.assertEqual(user.role, User.Roles.MERCHANT)

    def test_user_str_method(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.assertEqual(str(user), "test@example.com")


class RegisterSerializerTest(TestCase):
    def test_register_serializer_valid_data(self):
        from .serializers import RegisterSerializer

        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "role": User.Roles.CUSTOMER,
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.role, User.Roles.CUSTOMER)


class RegisterViewTest(APITestCase):
    def test_register_user(self):
        url = reverse(
            "register"
        )  # Assuming you have named the URL 'register' in urls.py
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "role": User.Roles.CUSTOMER,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["email"], "test@example.com")
        self.assertEqual(response.data["role"], User.Roles.CUSTOMER)

    def test_register_user_merchant(self):
        url = reverse("register")
        data = {
            "username": "merchantuser",
            "email": "merchant@example.com",
            "password": "testpass123",
            "role": User.Roles.MERCHANT,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["role"], User.Roles.MERCHANT)
