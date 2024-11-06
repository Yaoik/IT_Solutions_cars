import logging
from django.urls import reverse
from users.models import User
from rest_framework.test import APIRequestFactory, APITestCase
import random
import string
from .models import Car
from rest_framework import status


logger = logging.getLogger(__name__)

class TestCar(APITestCase):
    """Тесты эндпоинта cars"""

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
        register_url = reverse('users:register')
        user_data = self.create_user_data()
        self.user_1_token = self.client.post(register_url, user_data, format='json').json()['token']
        self.user_1:User = User.objects.get(email=user_data['email'])
        user_data = self.create_user_data()
        self.user_2_token = self.client.post(register_url, user_data, format='json').json()['token']
        self.user_2:User = User.objects.get(email=user_data['email'])
        
        self.cars_url = reverse('cars:car-list')  # Для списка
        self.car_detail_url = lambda car_id: reverse('cars:car-detail', args=[car_id])  # Для деталей

    def test_deleting_car(self):
        """Тесты с удалением модели Car."""
        
        car_data = self.create_car_data()
        response = self.client.post(self.cars_url, data=car_data, headers={'Authorization': f'Token {self.user_1_token}'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.json())
        car_id = response.json()['id']
        
        # Удаление чужой модели
        response = self.client.delete(self.car_detail_url(car_id), headers={'Authorization': f'Token {self.user_2_token}'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.json())
        
        # Удаление своей модели
        response = self.client.delete(self.car_detail_url(car_id), headers={'Authorization': f'Token {self.user_1_token}'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_create_car_error(self):
        """Тесты ошибок при создании"""
        
        # Создание без аккаунта
        car_data = self.create_car_data()
        response = self.client.post(self.cars_url, data=car_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.json())
        
        # Не указан Make
        car_data = self.create_car_data()
        del car_data['make']
        response = self.client.post(self.cars_url, data=car_data, headers={'Authorization': f'Token {self.user_1_token}'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('make', response.json())
        
        # Не указан description
        car_data = self.create_car_data()
        del car_data['description']
        response = self.client.post(self.cars_url, data=car_data, headers={'Authorization': f'Token {self.user_1_token}'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('description', response.json())
        
        # Не указан model
        car_data = self.create_car_data()
        del car_data['model']
        response = self.client.post(self.cars_url, data=car_data, headers={'Authorization': f'Token {self.user_1_token}'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('model', response.json())
        
    def test_create_car_success(self):
        """Тест успешного создания объекта Car."""
        car_data = self.create_car_data()
        response = self.client.post(self.cars_url, data=car_data, headers={'Authorization': f'Token {self.user_1_token}'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.json())
        
        # Создание без year
        car_data = self.create_car_data()
        del car_data['year']
        response = self.client.post(self.cars_url, data=car_data, headers={'Authorization': f'Token {self.user_1_token}'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.json())
        
    def test_update_car(self):
        """Тестирования изменения данных модели Car."""
        car_data = self.create_car_data()
        response = self.client.post(self.cars_url, data=car_data, headers={'Authorization': f'Token {self.user_1_token}'})
        car = Car.objects.get(id=response.json().get('id'))

        # Изменение модели
        data = car_data.copy()
        data['model'] = car.model + ' Новое'
        response = self.client.put(self.car_detail_url(car.id), data=data, headers={'Authorization': f'Token {self.user_1_token}'}) # type: ignore
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.json()['model'], car.model)
        
        # Изменение чужой модели Car
        data = car_data.copy()
        data['model'] = car.model + ' Другой пользователь'
        response = self.client.put(self.car_detail_url(car.id), data=data, headers={'Authorization': f'Token {self.user_2_token}'}) # type: ignore
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.json())