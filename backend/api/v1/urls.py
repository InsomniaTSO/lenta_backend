from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoriesViewSet

app_name = 'api_v1'

v1_router = DefaultRouter()
v1_router.register('categories', CategoriesViewSet, basename='categories')
# v1_router.register('sales', SalesViewSet, basename='sales')
# v1_router.register('shops', ShopsViewSet, basename='shops')
# v1_router.register('forecast', ForecastViewSet, basename='forecast')

urlpatterns = [
    path('', include(v1_router.urls)),
]
