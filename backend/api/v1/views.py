from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from categories.models import Category
from .serializers import CategoriesViewSerializer

class CategoriesViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление модели иерархии."""
    queryset = Category.objects.all()
    serializer_class = CategoriesViewSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
