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

    # def test_post_forecast(self):  
    #     """Тестирование создания прогноза с
    #     использованием метода POST.
    #     """
    
    # def test_post_forecast_missing_sku(self): 
    #     """Тестирование проверки на отсутствие "sku"."""

    
    # def test_post_forecast_invalid_sku(self): 
    #     """Тестирование проверки на недействительный SKU."""

  
    # def test_get_sales_without_filters(self):  
    #     """Тестирование получения прогнозов без использования фильтров."""
  
    # def test_store_filter(self):
    #     """Тестирование получения списка прогнозов с использованием фильтров."""


    def test_get_sales_invalid_method(self):
        """Тестирование попытки получить детализацию продажи, хотя это не разрешено.
        """
        response = self.client.get(self.url + str(self.forecast.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
