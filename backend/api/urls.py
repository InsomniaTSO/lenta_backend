from django.urls import include, path
from djoser.views import TokenDestroyView
from rest_framework.routers import DefaultRouter
from categories.v1.views import CategoriesViewSet
from users.views import CustomTokenCreateView

v1_router = DefaultRouter()
v1_router.register('categories', CategoriesViewSet, basename='categories')
# v1_router.register('sales', SalesViewSet, basename='sales')
# v1_router.register('shops', ShopsViewSet, basename='shops')
# v1_router.register('forecast', ForecastViewSet, basename='forecast')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('auth/token/login/', CustomTokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='logout'),
]