from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import City, Division, Format, Location, Shop, Size
from .serializers import ShopsSerializer


class ShopAPITests(APITestCase): 
    """Тестирование данных магазина.""" 
 
    def setUp(self): 
        # Создание тестовых данных 
        self.client = APIClient()
        self.city_1 = City.objects.create(city_id='test_city_1')
        self.city_2 = City.objects.create(city_id='test_city_2')
        self.division_1 = Division.objects.create(
            division_code_id='test_div_1'
        )
        self.division_2 = Division.objects.create(
            division_code_id='test_div_2'
        )
        self.format_1 = Format.objects.create(type_format_id=1)
        self.format_2 = Format.objects.create(type_format_id=2)
        self.location_1 = Location.objects.create(type_loc_id=1)
        self.location_2 = Location.objects.create(type_loc_id=2)
        self.size_1 = Size.objects.create(type_size_id=1)
        self.size_2 = Size.objects.create(type_size_id=2)
        self.shop_1 = Shop.objects.create(
            store='store1',
            city=self.city_1,
            division=self.division_1,
            type_format=self.format_1,
            loc=self.location_1,
            size=self.size_1,
            is_active=1
        )
        self.shop_2 = Shop.objects.create(
            store='store2',
            city=self.city_2,
            division=self.division_2,
            type_format=self.format_2,
            loc=self.location_2,
            size=self.size_2,
            is_active=0
        )
        self.url = reverse('shops-list')

    def test_get_all_shops(self):
        """Тест на получение списка всех магазинов."""
        response = self.client.get(self.url)
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка количества возвращенных магазинов
        self.assertEqual(len(response.data['data']), 2)
        # Проверка правильности данных
        serializer = ShopsSerializer([self.shop_1, self.shop_2], many=True)
        self.assertEqual(response.data['data'], serializer.data)

    def test_store_filter(self):
        """Тест фильтрации магазина по store."""
        response = self.client.get(self.url, {'store': 'store1'})
        serializer = ShopsSerializer(self.shop_1)
        response_data = [dict(item) for item in response.data['data']]
        self.assertEqual(response_data, [serializer.data])

    def test_city_filter(self):
        """Тест фильтрации магазина по city."""
        response = self.client.get(self.url, {'city': 'test_city_1'})
        serializer = ShopsSerializer(self.shop_1)
        response_data = [dict(item) for item in response.data['data']]
        self.assertEqual(response_data, [serializer.data])

    def test_division_filter(self):
        """Тест фильтрации магазина по division."""
        response = self.client.get(self.url, {'division': 'test_div_1'})
        serializer = ShopsSerializer(self.shop_1)
        response_data = [dict(item) for item in response.data['data']]
        self.assertEqual(response_data, [serializer.data])

    def test_format_filter(self):
        """Тест фильтрации магазина по type_format."""
        response = self.client.get(self.url, {'type_format': 1})
        serializer = ShopsSerializer(self.shop_1)
        response_data = [dict(item) for item in response.data['data']]
        self.assertEqual(response_data, [serializer.data])

    def test_location_filter(self):
        """Тест фильтрации магазина по loc."""
        response = self.client.get(self.url, {'loc': 1})
        serializer = ShopsSerializer(self.shop_1)
        response_data = [dict(item) for item in response.data['data']]
        self.assertEqual(response_data, [serializer.data])

    def test_size_filter(self):
        """Тест фильтрации магазина по size."""
        response = self.client.get(self.url, {'size': 1})
        serializer = ShopsSerializer(self.shop_1)
        response_data = [dict(item) for item in response.data['data']]
        self.assertEqual(response_data, [serializer.data])

    def test_is_active_filter(self):
        """Тест фильтрации магазина по  флагу is_active."""
        response = self.client.get(self.url, {'is_active': 1})
        serializer = ShopsSerializer(self.shop_1)
        response_data = [dict(item) for item in response.data['data']]
        self.assertEqual(response_data, [serializer.data])
