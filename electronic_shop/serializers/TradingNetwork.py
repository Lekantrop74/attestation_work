from rest_framework import serializers
from electronic_shop.models import TradingNetwork


class TradingNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingNetwork
        fields = '__all__'
