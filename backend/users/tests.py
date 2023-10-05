from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import User

class CustomUserTests(APITestCase): 

    def setUp(self): 
        # Создание тестовых данных 
        self.register_url = reverse('login')
        self.token_url = reverse('login')

    def test_create_user(self): 
        # Тест успешного создания пользователя 
        data = { 
            'username': 'testuser', 
            'email': 'testuser@example.com', 
            'first_name': 'Test', 
            'last_name': 'User', 
            'password': 'testpassword' 
        } 
        response = self.client.post(self.register_url, data, format='json') 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 
        self.assertEqual(response.data['username'], 'testuser')

    # def test_create_user_forbidden_name(self): 
    #     # Тест на попытку создания пользователя с запрещенным именем 
    #     data = { 
    #         'username': 'forbiddenname',
    #         'email': 'testuser2@example.com', 
    #         'first_name': 'Test', 
    #         'last_name': 'User', 
    #         'password': 'testpassword' 
    #     } 
    #     response = self.client.post(self.register_url, data, format='json') 
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_get_token(self): 
    #     # Тест получения токена 
    #     User.objects.create_user(email='testuser3@example.com', password='testpassword', username='testuser3') 
    #     data = { 
    #         'email': 'testuser3@example.com', 
    #         'password': 'testpassword' 
    #     } 
    #     response = self.client.post(self.token_url, data, format='json') 
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED) 
    #     self.assertIn('token', response.data)

    # def test_get_token_invalid_credentials(self): 
    #     # Тест получения токена с некорректными учетными данными 
    #     data = { 
    #         'email': 'wronguser@example.com', 
    #         'password': 'wrongpassword' 
    #     } 
    #     response = self.client.post(self.token_url, data, format='json') 
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_get_token_inactive_user(self): 
    #     # Тест на попытку получения токена для неактивного пользователя 
    #     user = User.objects.create_user(email='inactiveuser@example.com', password='testpassword', username='inactiveuser') 
    #     user.is_active = False 
    #     user.save() 
    #     data = { 
    #         'email': 'inactiveuser@example.com', 
    #         'password': 'testpassword' 
    #     } 
    #     response = self.client.post(self.token_url, data, format='json') 
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)