import logging
from django.urls import reverse
from users.models import User
from rest_framework.test import APIRequestFactory, APITestCase
import random
import string
from .models import Car
from rest_framework import status


logger = logging.getLogger(__name__)

class TestComments(APITestCase):
    """Тесты эндпоинта comments"""

    def create_car_data(self):
        makes = ["Toyota", "Ford", "Honda"]
        models = ["Camry", "Mustang", "Civic"]
        years = [i for i in range(1900, 2024, 1)]
        description = ''.join(random.choices(string.ascii_letters, k=15) + random.choices('1234567890', k=3)) * 5
        user_data = {
            'make': random.choice(makes),
            'model': random.choice(models),
            'year': random.choice(years),
            'description': description,
        }
        return user_data
    
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
        register_url = reverse('users:register') # регистрация User
        
        user_data = self.create_user_data()
        self.user_1_token = self.client.post(register_url, user_data, format='json').json()['token']
        self.user_1:User = User.objects.get(email=user_data['email'])
        user_data = self.create_user_data()
        self.user_2_token = self.client.post(register_url, user_data, format='json').json()['token']
        self.user_2:User = User.objects.get(email=user_data['email'])
        
        self.cars_url = reverse('cars:car-list') # Для списка
        self.car_detail_url = lambda car_id: reverse('cars:car-detail', args=[car_id]) # Для деталей
        
        self.comments_url = lambda car_id: reverse('cars:comments:comment-list', kwargs={'car_id': car_id}) # Для списка
        self.comment_detail_url = lambda car_id, comment_id: reverse('cars:comments:comment-detail', kwargs={'car_id': car_id, 'pk': comment_id}) # Для деталей
        
        self.client.post(self.cars_url, data=self.create_car_data(), headers={'Authorization': f'Token {self.user_1_token}'})
        self.client.post(self.cars_url, data=self.create_car_data(), headers={'Authorization': f'Token {self.user_2_token}'})

    def test_create_comment_error(self):
        """Тесты ошибок создания модели Comment."""
        
        car_id = Car.objects.first().id # type: ignore
        comment_1_id = self.client.post(self.comments_url(car_id), data={'content': 'Первый коммет!'}, headers={'Authorization': f'Token {self.user_2_token}'}).json()['id']
        
        # Не авторизован
        responce = self.client.post(self.comments_url(car_id), data={'content': 'Первый коммет!'})
        self.assertEqual(responce.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', responce.json())
           
        # Нет контента
        responce = self.client.post(self.comments_url(car_id), data={})
        self.assertEqual(responce.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', responce.json())

    def test_read_comment_error(self):
        """Тесты ошибок просмотра комментария по id"""
        car_id = Car.objects.first().id # type: ignore
        responce = self.client.post(self.comments_url(car_id), data={'content': 'Первый коммет!'}, headers={'Authorization': f'Token {self.user_2_token}'})
        comment_1_id = responce.json()['id']
        
        responce = self.client.get(self.comment_detail_url(car_id, comment_1_id))
        self.assertEqual(responce.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', responce.json())


    def test_create_comment_success(self):
        """Тесты создания модели Comment."""
        car_id = Car.objects.first().id # type: ignore
        
        # Создание коммента
        responce = self.client.post(self.comments_url(car_id), data={'content': 'Первый коммет!'}, headers={'Authorization': f'Token {self.user_2_token}'})
        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', responce.json())
        self.assertEqual(self.user_2.username, responce.json()['author'])
        
        # Создание коммента другим пользователем
        responce = self.client.post(self.comments_url(car_id), data={'content': 'Первый коммет!'}, headers={'Authorization': f'Token {self.user_1_token}'})
        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', responce.json())
        self.assertEqual(self.user_1.username, responce.json()['author'])
        
        comment_1_id = responce.json()['id']
        
        # Просмотр списка комментов
        responce = self.client.get(self.comments_url(car_id))
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(len(responce.json()), 2)