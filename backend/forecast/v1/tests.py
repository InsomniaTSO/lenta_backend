from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from categories.v1.models import Category, Group, Product, Subcategory
from shops.v1.models import City, Division, Format, Location, Size, Shop

from .models import Forecast
from .serializers import ForecastGetSerializer


class ForecastAPITests(APITestCase):
    """Тестирование API прогноза."""

    def setUp(self):
        self.client = APIClient()
        # Создание тестового пользователя
        # self.user = User.objects.create_user(
        #     username='testuser',
        #     email='testuser@example.com',
        #     first_name='first_name',
        #     last_name='last_name',
        #     password='testpass',

        # )
        # self.client.login(
        #     email='testuser@example.com',
        #     password='testpass'
        # )
        # token_response = self.client.post(reverse('login'), data={
        #     'email': 'testuser@example.com',
        #     'password': 'testpass'
        # })
        # self.token = token_response.data['auth_token']
        # self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        # Создание тестовых данных для магазина
        self.city = City.objects.create(city_id='test_city')
        self.division = Division.objects.create(division_code_id='test_div')
        self.format = Format.objects.create(type_format_id=1)
        self.location = Location.objects.create(type_loc_id=1)
        self.size = Size.objects.create(type_size_id=1)
        self.shop = Shop.objects.create(
            store='store_test',
            city=self.city,
            division=self.division,
            type_format=self.format,
            loc=self.location,
            size=self.size, is_active=1
        )
        self.shop_2 = Shop.objects.create(
            store='store_test_2',
            city=self.city,
            division=self.division,
            type_format=self.format,
            loc=self.location,
            size=self.size, is_active=0
        )

        # Создание тестовых данных для продукта
        self.group = Group.objects.create(group_id='test_group')
        self.category = Category.objects.create(cat_id='test_cat')
        self.subcategory = Subcategory.objects.create(subcat_id='test_subcat')
        self.product = Product.objects.create(
            sku='sku_test', group=self.group,
            category=self.category, subcategory=self.subcategory,
            uom=1)
        self.product_2 = Product.objects.create(
            sku='sku_test_2', group=self.group,
            category=self.category, subcategory=self.subcategory,
            uom=17
        )

        # Создание тестовых данных для прогноза
        self.forecast = Forecast.objects.create(
            store=self.shop,
            product=self.product,
            forecast_date='2023-10-01',
            date='2023-10-01',
            target=10
        )
        self.forecast_2 = Forecast.objects.create(
            store=self.shop_2,
            product=self.product_2,
            forecast_date='2023-10-01',
            date='2023-10-02',
            target=20
        )
        self.url = reverse('forecast-list')

    def test_get_forecasts_with_valid_params(self):
        """Тестирование запроса с допустимыми параметрами.
        """
        url = (
            reverse('forecast-list') + '?store={}&sku={}'.format(
                self.shop.store, self.product.sku
            )
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('data' in response.data)
        self.assertTrue(response.data['data'])
        self.assertEqual(response.data['data'][0]['store'], self.shop.store)
        self.assertEqual(response.data['data'][0]['sku'], self.product.sku)

    def test_get_forecasts_with_invalid_params(self):
        """Тестирование запроса с недопустимыми параметрами.
        """
        url = reverse('forecast-list') + '?store=nonexistent&sku=nonexistent'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_forecasts_without_params(self):
        """Тестирование запроса без параметров.
        """
        url = reverse('forecast-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_sales_invalid_method(self):
        """Тестирование попытки получить детализацию продажи,
        хотя это не разрешено.
        """
        response = self.client.get(self.url + str(self.forecast.id) + '/')
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    # def test_create_forecast_successfully(self):
    # # Подготовка данных для POST-запроса
    #     post_data = {
    #         'data': {
    #             'store': self.shop.store,
    #             'product': self.product.sku,
    #             'forecast_date': '2023-10-03',
    #             'date': '2023-10-03',
    #             'target': 15
    #         }
    #     }
    #     response = self.client.post(self.url, post_data, format='json')
    #     print(response)
    #     self.assertEqual(
    #         response.status_code, status.HTTP_201_CREATED
    #     )
    #     self.assertTrue('store' in response.data)
    #     self.assertEqual(response.data['store'], post_data['data']['store'])

    # def test_create_forecast_with_invalid_data(self):
    #     # Подготовка данных с недопустимым значением
    #        (например, недопустимый id магазина)
    #     post_data = {
    #         'data': {
    #             'store': 99999,  # недопустимый ID
    #             'product': self.product.sku,
    #             'forecast_date': '2023-10-03',
    #             'date': '2023-10-03',
    #             'target': 15
    #         }
    #     }
    #     response = self.client.post(self.url, post_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_forecast_missing_fields(self):
    #     # Подготовка данных без поля 'date'
    #     post_data = {
    #         'data': {
    #             'store': self.shop.store,
    #             'product': self.product.sku,
    #             'forecast_date': '2023-10-03',
    #             'target': 15
    #         }
    #     }
    #     response = self.client.post(self.url, post_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
