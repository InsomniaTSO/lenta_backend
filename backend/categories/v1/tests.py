from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from categories.v1.models import Group, Category, Subcategory, Product
from categories.v1.serializers import ProductSerializer

class ProductAPITests(APITestCase):
    """Тестирование данных товарной иерархии.
    """

    def setUp(self):
        # Создание тестовых данных
        self.client = APIClient()
        self.group_1 = Group.objects.create(group_id = 'test_group_1')
        self.group_2 = Group.objects.create(group_id = 'test_group_2')
        self.category_1 = Category.objects.create(cat_id = 'test_cat_1')
        self.category_2 = Category.objects.create(cat_id = 'test_cat_2')
        self.subcategory_1 = Subcategory.objects.create(subcat_id = 'test_subcat_1')
        self.subcategory_2 = Subcategory.objects.create(subcat_id = 'test_subcat_2')
        self.product_1 = Product.objects.create(sku='sku1', group=self.group_1, category=self.category_1, subcategory=self.subcategory_1, uom=1)
        self.product_2 = Product.objects.create(sku='sku2', group=self.group_2, category=self.category_2, subcategory=self.subcategory_2, uom=0)
        self.url = reverse('categories-list')

    def test_get_all_products(self):
        """Тест на получение списка всех продуктов."""
        response = self.client.get(self.url)
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка количества возвращенных продуктов
        self.assertEqual(len(response.data['data']), 2)
        # Проверка правильности данных
        serializer = ProductSerializer([self.product_1, self.product_2], many=True)
        self.assertEqual(response.data['data'], serializer.data)

    def test_sku_filter(self):
        """Тест фильтрации продукта по sku."""
        response = self.client.get(self.url, {'sku': 'sku1'})
        serializer = ProductSerializer(self.product_1)
        response_data = [dict(item) for item in response.data['data']]
        self.assertEqual(response_data, [serializer.data])

    def test_group_filter(self):
        """Тест фильтрации продукта по группе."""
        response = self.client.get(self.url, {'group': self.group_1.group_id})
        serializer = ProductSerializer(self.product_1)
        response_data = [dict(item) for item in response.data['data']]
        self.assertEqual(response_data, [serializer.data])

    def test_category_filter(self):
        """Тест фильтрации продукта по категории."""
        response = self.client.get(self.url, {'category': self.category_1.cat_id})
        serializer = ProductSerializer(self.product_1)
        response_data = [dict(item) for item in response.data['data']]
        self.assertEqual(response_data, [serializer.data])

    def test_subcategory_filter(self):
        """Тест фильтрации продукта по подкатегории."""
        response = self.client.get(self.url, {'subcategory': self.subcategory_1.subcat_id})
        serializer = ProductSerializer(self.product_1)
        response_data = [dict(item) for item in response.data['data']]
        self.assertEqual(response_data, [serializer.data])

    def test_uom_filter(self):
        """Тест фильтрации продукта по uom."""
        response = self.client.get(self.url, {'uom': 1})
        serializer = ProductSerializer(self.product_1)
        response_data = [dict(item) for item in response.data['data']]
        self.assertEqual(response_data, [serializer.data])
