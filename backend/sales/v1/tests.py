from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Shop
from shops.v1.models import City, Division, Format, Location, Size
from categories.v1.models import Group, Category, Subcategory, Product
from .models import Sales


class SalesAPITests(APITestCase):
    """Тестирование API продаж.
    """
    
    def setUp(self):
        # Создание тестовых данных для магазина
        self.city = City.objects.create(city_id='test_city')
        self.division = Division.objects.create(division_code_id='test_div')
        self.format = Format.objects.create(type_format_id=1)
        self.location = Location.objects.create(type_loc_id=1)
        self.size = Size.objects.create(type_size_id=1)
        self.shop = Shop.objects.create(store='store_test', city=self.city, division=self.division, 
                                        type_format=self.format, loc=self.location, 
                                        size=self.size, is_active=1)
        
        # Создание тестовых данных для продукта
        self.group = Group.objects.create(group_id = 'test_group')
        self.category = Category.objects.create(cat_id = 'test_cat')
        self.subcategory = Subcategory.objects.create(subcat_id = 'test_subcat')
        self.product = Product.objects.create(sku='sku_test', group=self.group, 
                                              category=self.category, subcategory=self.subcategory, 
                                              uom=1)

        # Создание тестовых данных для продаж
        self.sales = Sales.objects.create(
            shop=self.shop,
            product=self.product,
            date="2023-10-05",
            sales_type=1,
            sales_units=10,
            sales_units_promo=5,
            sales_rub=1000.00,
            sales_run_promo=500.00
        )
        self.url = reverse('sales-list')

    # def test_get_sales(self):
    #     """Тестирование получения списка продаж.
    #     """
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)
    # #     self.assertEqual(response.data[0]['sales_units'], 10)

    # def test_post_sales(self):
    #     """Тестирование создания продажи через метод POST.
    #     """
    #     data = {
    #         "shop": self.shop.id,
    #         "product": self.product.id,
    #         "date": "2023-10-06",
    #         "sales_type": 1, 
    #         "sales_units": 15,
    #         "sales_units_promo": 7,
    #         "sales_rub": 1500.00,
    #         "sales_run_promo": 700.00
    #     }
    #     response = self.client.post(self.url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Sales.objects.count(), 2)
    #     self.assertEqual(Sales.objects.latest('id').sales_units, 15)

    def test_get_sales_with_filters(self):
        """Тестирование получения списка продаж с применением фильтров.
        """
        response = self.client.get(self.url, {'store': self.shop.store, 'sku': self.product.sku})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['sales_units'], 10)

    # def test_get_sales_no_data(self):
    #     """Тестирование получения списка продаж с неверными параметрами фильтрации.
    #     """
    #     response = self.client.get(self.url, {'store': 999, 'sku': 999})  # Несуществующие ID
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['error'], 'Не найдены данные с указанными параметрами')

    # def test_get_sales_invalid_method(self):
    #     """Тестирование попытки получить детализацию продажи, хотя это не разрешено.
    #     """
    #     response = self.client.get(self.url + str(self.sales.id) + '/')
    #     self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)