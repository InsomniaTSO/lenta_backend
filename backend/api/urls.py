from django.urls import include, path
from djoser.views import TokenDestroyView
from rest_framework.routers import DefaultRouter

from categories.views import ProductViewSet
from forecast.views import ForecastViewSet
from sales.views import SalesViewSet
from shops.views import ShopViewSet
from users.views import CustomTokenCreateView, CustomUserViewSet

v1_router = DefaultRouter()
v1_router.register("users", CustomUserViewSet, basename="user")
v1_router.register("categories", ProductViewSet, basename="categories")
v1_router.register("sales", SalesViewSet, basename="sales")
v1_router.register("shops", ShopViewSet, basename="shops")
v1_router.register("forecast", ForecastViewSet, basename="forecast")

urlpatterns = [
    path("v1/", include(v1_router.urls)),
    path("auth/token/login/", CustomTokenCreateView.as_view(), name="login"),
    path("auth/token/logout/", TokenDestroyView.as_view(), name="logout"),
]
