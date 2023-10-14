from rest_framework import serializers

from electronic_shop.models import NetworkUnit


class NetworkUnitSerializer(serializers.ModelSerializer):
    debt_to_supplier = serializers.ReadOnlyField()  # Устанавливаем поле как read-only

    class Meta:
        model = NetworkUnit
        fields  = '__all__'
