from django.test import TestCase
import logging
from django.urls import reverse
from rest_framework import status
from users.models import User
from rest_framework.exceptions import ValidationError
from users.serializers import RegisterSerializer, CustomAuthTokenSerializer
from rest_framework.test import APIRequestFactory, APITestCase
import random
import string

logger = logging.getLogger(__name__)

class TestUserRegister(APITestCase):
    """Тесты эндпоинта register"""

    def create_user_data(self):
        password = ''.join(random.choices(string.ascii_letters, k=15) + random.choices('1234567890', k=3))
        num = User.objects.count() + 1
        user_data = {
            'username':f'test_user_{num}', 
            'email':f'test_email_{num}@gmail.com', 
            'password':password, 
            'password2':password
        }
        return user_data
        
    def setUp(self):
        self.register_url = reverse('users:register')  # Убедитесь, что путь в urls.py назван как 'register'
        self.client.post(self.register_url, self.create_user_data(), format='json')
        self.test_user:User = User.objects.first() # type:ignore
    
    def test_register_user_success(self):
        """Тест успешной регистрации пользователя."""
        user_data = self.create_user_data()
        response = self.client.post(self.register_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.json())
        self.assertIn("token", response.json())
        self.assertEqual(User.objects.count(), 2)

    def test_register_user_error(self):
        """Тест ошибок регистрации пользователя."""
        user_data = self.create_user_data()
        
        # Несовпадение паролей
        data = user_data.copy()
        data['password2'] = '123321'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.json())
        
        # Невалидный Email
        data = user_data.copy()
        data['email'] = 'email123'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.json())
        
        # Простой пароль
        data = user_data.copy()
        data['password'] = '123'
        data['password2'] = '123'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.json())
        
        # Дубликат пользователя
        data = user_data.copy()
        response = self.client.post(self.register_url, data, format='json')
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.json())
        self.assertIn("username", response.json())