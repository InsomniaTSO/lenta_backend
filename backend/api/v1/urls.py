from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('sales/', views.SalesListView.as_view(), name='sales-list'),
    path('shops/', views.ShopListView.as_view(), name='shop-list'),
    path('forecast/', views.ForecastCreateView.as_view(), name='forecast-create'),
]
