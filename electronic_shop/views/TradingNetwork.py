from rest_framework.viewsets import ModelViewSet
from electronic_shop.models import TradingNetwork
from electronic_shop.permissions.permissions import IsActiveUser
from electronic_shop.serializers.TradingNetwork import TradingNetworkSerializer


class TradingNetworkViewSet(ModelViewSet):
    queryset = TradingNetwork.objects.all()
    serializer_class = TradingNetworkSerializer
    permission_classes = [IsActiveUser]
