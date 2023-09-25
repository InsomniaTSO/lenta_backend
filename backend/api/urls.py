from django.urls import include, path
from rest_framework.routers import DefaultRouter
from categories.views import CategoriesViewSet

v1_router = DefaultRouter()
v1_router.register('categories', CategoriesViewSet, basename='categories')
# v1_router.register('sales', SalesViewSet, basename='sales')
# v1_router.register('shops', ShopsViewSet, basename='shops')
# v1_router.register('forecast', ForecastViewSet, basename='forecast')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
