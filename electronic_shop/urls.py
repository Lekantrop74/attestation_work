from django.urls import path, include
from rest_framework.routers import DefaultRouter

from electronic_shop.apps import ElectronicShopConfig
from electronic_shop.views.NetworkUnit import NetworkUnitViewSet
from electronic_shop.views.Product import ProductViewSet
from electronic_shop.views.TradingNetwork import TradingNetworkViewSet

app_name = ElectronicShopConfig.name

router = DefaultRouter()
router.register(r'Product', ProductViewSet)
router.register(r'TradingNetwork', TradingNetworkViewSet)
router.register(r'NetworkUnit', NetworkUnitViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]