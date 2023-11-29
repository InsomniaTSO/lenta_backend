from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from categories.models import Category, Group, Product, Subcategory
from shops.models import City, Division, Format, Location, Size

from sales.models import Sales, Shop
from users.models import User


class SalesAPITests(APITestCase):
    """Тестирование API продаж."""

    def setUp(self):
        # Создание тестовых данных
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            first_name="first_name",
            last_name="last_name",
            password="testpass",
        )
        self.client.login(email="testuser@example.com", password="testpass")
        token_response = self.client.post(
            reverse("login"),
            data={"email": "testuser@example.com", "password": "testpass"},
        )
        self.token = token_response.data["auth_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

        # Создание тестовых данных для магазина
        self.city = City.objects.create(city_id="test_city")
        self.division = Division.objects.create(division_code_id="test_div")
        self.format = Format.objects.create(type_format_id=1)
        self.location = Location.objects.create(type_loc_id=1)
        self.size = Size.objects.create(type_size_id=1)
        self.shop = Shop.objects.create(
            store="store_test",
            city=self.city,
            division=self.division,
            type_format=self.format,
            loc=self.location,
            size=self.size,
            is_active=1,
        )

        # Создание тестовых данных для продукта
        self.group = Group.objects.create(group_id="test_group")
        self.category = Category.objects.create(cat_id="test_cat")
        self.subcategory = Subcategory.objects.create(subcat_id="test_subcat")
        self.product = Product.objects.create(
            sku="sku_test",
            group=self.group,
            category=self.category,
            subcategory=self.subcategory,
            uom=1,
        )

        # Создание тестовых данных для продаж
        self.sales = Sales.objects.create(
            shop=self.shop,
            product=self.product,
            date="2023-10-05",
            sales_type=1,
            sales_units=10,
            sales_units_promo=5,
            sales_rub=1000.00,
            sales_run_promo=500.00,
        )
        self.url = reverse("sales-list")

    def test_get_sales(self):
        """Тестирование получения списка продаж без фильтров."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_sales(self):
        """Тестирование создания продажи через метод POST."""
        data = {
            "data": {
                "store": self.shop.store,
                "sku": self.product.sku,
                "fact": [
                    {
                        "date": "2023-10-06",
                        "sales_type": 1,
                        "sales_units": 15,
                        "sales_units_promo": 7,
                        "sales_rub": 1500.00,
                        "sales_run_promo": 700.00,
                    }
                ],
            }
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sales.objects.count(), 2)
        self.assertEqual(Sales.objects.latest("id").sales_units, 15)

    def test_get_sales_with_filters(self):
        """Тестирование получения списка продаж с применением фильтров."""
        response = self.client.get(
            self.url, {"store": self.shop.store, "sku": self.product.sku}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data["data"][0]["fact"][0]["sales_units"], 10)

    def test_get_sales_no_data(self):
        """Тестирование получения списка продаж с
        неверными параметрами фильтрации.
        """
        response = self.client.get(self.url, {"store": 999, "sku": 999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_sales_invalid_method(self):
        """Тестирование попытки получить детализацию продажи,
        хотя это не разрешено.
        """
        response = self.client.get(self.url + str(self.sales.id) + "/")
        self.assertEqual(response.status_code, 
                         status.HTTP_405_METHOD_NOT_ALLOWED)
