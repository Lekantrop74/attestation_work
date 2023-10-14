from rest_framework.viewsets import ModelViewSet

from electronic_shop.models import Product
from electronic_shop.permissions.permissions import IsActiveUser
from electronic_shop.serializers.Product import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveUser]
