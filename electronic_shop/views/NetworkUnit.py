from rest_framework.viewsets import ModelViewSet
from electronic_shop.models import NetworkUnit
from electronic_shop.permissions.permissions import IsActiveUser
from electronic_shop.serializers.NetworkUnit import NetworkUnitSerializer


class NetworkUnitViewSet(ModelViewSet):
    queryset = NetworkUnit.objects.all()
    serializer_class = NetworkUnitSerializer
    permission_classes = [IsActiveUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        # Добавьте фильтрацию по стране, если задан параметр 'country' в запросе
        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(country=country)
        return queryset
