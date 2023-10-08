from rest_framework import serializers

from shops.v1.models import Shop


class ShopsSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов магазинов.
    Предоставляет подробную информацию о каждом магазине,
    включая id магазина, город, подразделение, формат,
    локацию, размер и статус активности.
    """

    city = serializers.ReadOnlyField(source='city.city_id')
    division = serializers.ReadOnlyField(source='division.division_code_id')
    type_format = serializers.ReadOnlyField(
        source='type_format.type_format_id'
    )
    loc = serializers.ReadOnlyField(source='loc.type_loc_id')
    size = serializers.ReadOnlyField(source='size.type_size_id')

    class Meta:
        model = Shop
        fields = ('store', 'city',
                  'division', 'type_format',
                  'loc', 'size',
                  'is_active')
