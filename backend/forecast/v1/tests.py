from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from categories.v1.models import Category, Group, Product, Subcategory
from shops.v1.models import City, Division, Format, Location, Size, Shop

from .models import Forecast
from .serializers import ForecastGetSerializer


class ForecastAPITests(APITestCase):  
    """Тестирование API прогноза."""  
      
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
        self.shop_2 = Shop.objects.create(store='store_test_2', city=self.city, division=self.division,   
                                        type_format=self.format, loc=self.location,   
                                        size=self.size, is_active=0) 
          
        # Создание тестовых данных для продукта  
        self.group = Group.objects.create(group_id='test_group')  
        self.category = Category.objects.create(cat_id='test_cat')  
        self.subcategory = Subcategory.objects.create(subcat_id='test_subcat')  
        self.product = Product.objects.create(sku='sku_test', group=self.group,   
                                              category=self.category, subcategory=self.subcategory,   
                                              uom=1) 
        self.product_2 = Product.objects.create(sku='sku_test_2', group=self.group,   
                                              category=self.category, subcategory=self.subcategory,   
                                              uom=17)  
  
  
        # Создание тестовых данных для прогноза  
        self.forecast_data = { 
            'sku': self.product.sku, 
            'sales_units': {  
                '2023-10-01': 102, 
                '2023-10-02': 107, 
                '2023-10-03': 112, 
                '2023-10-04': 117, 
                '2023-10-05': 122, 
                '2023-10-06': 127, 
                '2023-10-07': 132, 
                '2023-10-08': 137, 
                '2023-10-09': 142, 
                '2023-10-10': 147, 
                '2023-10-11': 152, 
                '2023-10-12': 157, 
                '2023-10-13': 162, 
                '2023-10-14': 167 
                } 
            } 
        self.forecast_data_2 = { 
            'sku': self.product_2.sku, 
            'sales_units': {  
                '2023-10-01': 102, 
                '2023-10-02': 107, 
                '2023-10-03': 112, 
                '2023-10-04': 117, 
                '2023-10-05': 122, 
                '2023-10-06': 127, 
                '2023-10-07': 132, 
                '2023-10-08': 137, 
                '2023-10-09': 142, 
                '2023-10-10': 147, 
                '2023-10-11': 152, 
                '2023-10-12': 157, 
                '2023-10-13': 162, 
                '2023-10-14': 167 
                } 
            } 
        self.forecast = Forecast.objects.create(  
            store=self.shop, 
            product=self.product, 
            forecast_date='2023-10-01',  
            forecast=self.forecast_data 
        ) 
        self.forecast_2 = Forecast.objects.create(  
            store=self.shop_2, 
            product=self.product_2, 
            forecast_date='2023-10-01',  
            forecast=self.forecast_data_2 
        ) 
        self.url = reverse('forecast-list')

    def test_post_forecast(self):  
        """Тестирование создания прогноза с
        использованием метода POST.
        """
        data = { 
            'store': self.shop.store, 
            'forecast_date': '2023-10-02', 
            'forecast': { 
                'sku': self.product.sku, 
                'sales_units': {  
                    '2023-10-02': 102, 
                    '2023-10-03': 107, 
                    '2023-10-04': 112, 
                    '2023-10-05': 117, 
                    '2023-10-06': 122, 
                    '2023-10-07': 127, 
                    '2023-10-08': 132, 
                    '2023-10-09': 137, 
                    '2023-10-10': 142, 
                    '2023-10-11': 147, 
                    'd2023-10-12': 152, 
                    '2023-10-13': 157, 
                    '2023-10-14': 162, 
                    '2023-10-15': 167 
                } 
            } 
        } 
        response = self.client.post(self.url, data, format='json') 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 
    
    def test_post_forecast_missing_sku(self): 
        """Тестирование проверки на отсутствие "sku"."""
        data = { 
            'store': self.shop.store, 
            'forecast_date': '2023-10-02', 
            'forecast': {} 
        } 
        response = self.client.post(self.url, data, format='json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        self.assertIn('forecast', response.data) 
    
    def test_post_forecast_invalid_sku(self): 
        """Тестирование проверки на недействительный SKU."""
        data = { 
            'store': self.shop.store, 
            'forecast_date': '2023-10-02', 
            'forecast': { 
                'sku': 'invalid_sku', 
                'sales_units': { 
                    '2023-10-02': 102 
                } 
            } 
        } 
        response = self.client.post(self.url, data, format='json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        self.assertIn('sku', response.data) 
    
    def test_post_forecast_missing_sales_units(self): 
        """Тестирование проверки на отсутствие "sales_units"."""
        data = { 
            'store': self.shop.store, 
            'forecast_date': '2023-10-02', 
            'forecast': { 
                'sku': self.product.sku 
            } 
        } 
        response = self.client.post(self.url, data, format='json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        self.assertIn('forecast', response.data) 
    
    def test_get_sales_without_filters(self):  
        """Тестирование получения прогнозов без использования фильтров."""
        response = self.client.get(self.url)  
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  
  
    def test_store_filter(self):
        """Тестирование получения списка прогнозов с использованием фильтров."""
        response = self.client.get(self.url, {'store': 'store_test_2', 'sku': 'sku_test_2'}).json()
        serializer_data = ForecastGetSerializer(self.forecast_2).data
        for item in response['data']:
            self.assertEqual(item['forecast'], serializer_data['forecast'])
            self.assertEqual(item['forecast_date'], serializer_data['forecast_date'])
            self.assertEqual(item['store'], serializer_data['store'])
        
    def test_get_sales_invalid_method(self):
        """Тестирование попытки получить детализацию продажи, хотя это не разрешено.
        """
        response = self.client.get(self.url + str(self.forecast.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
