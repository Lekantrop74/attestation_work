from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from users.models import Users
from .models import NetworkUnit, TradingNetwork, Product


class NetworkUnitViewSetTests(APITestCase):
    def setUp(self):
        # Создаем пользователя и токен для авторизации
        self.user = Users(
            email="test@gmail.com",
            password="test",
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )

        self.user.set_password("test")
        self.user.save()

        self.client = APIClient()
        token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        self.trading_network = TradingNetwork.objects.create(title="Тестовая сеть")
        self.product = Product.objects.create(title="Тестовый продукт", model="Модель", release_date="2023-01-01")
        self.unit = NetworkUnit.objects.create(
            level=1,  # Розничная сеть
            name="Тестовое звено",
            email="test@example.com",
            country="Тестовая страна",
            city="Тестовый город",
            street="Тестовая улица",
            house_number="123",
            trading_network=self.trading_network,
        )
        self.unit.products.add(self.product)


    def test_list_network_units(self):
        # Тест на получение списка NetworkUnit
        url = "/drf/api/NetworkUnit/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Проверяем, что получили две записи

    def test_create_network_unit(self):
        # Тест на создание NetworkUnit
        data = {
            "level": 1,
            "name": "Новое звено",
            "email": "new@example.com",
            "country": "Новая страна",
            "city": "Новый город",
            "street": "Новая улица",
            "house_number": "456",
            "trading_network": self.trading_network.id,
            "products": [self.product.id],
        }
        url = "/drf/api/NetworkUnit/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NetworkUnit.objects.count(), 2)  # Проверяем, что количество записей увеличилось


    def test_filter_network_units_by_country(self):
        # Тест на фильтрацию NetworkUnit по стране
        another_unit = NetworkUnit.objects.create(
            level=1,
            name="Другое звено",
            email="another@example.com",
            country="Другая страна",
            city="Другой город",
            street="Другая улица",
            house_number="789",
            trading_network=self.trading_network,
        )
        url = f"/drf/api/NetworkUnit/?country={self.unit.country}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Проверяем, что получили одну запись

    def test_update_network_unit(self):
        # Тест на обновление NetworkUnit
        updated_name = "Обновленное звено"
        data = {
            "name": updated_name,
        }
        url = f"/drf/api/NetworkUnit/{self.unit.id}/"
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.unit.refresh_from_db()  # Обновляем объект из базы данных
        self.assertEqual(self.unit.name, updated_name)  # Проверяем, что имя было обновлено

    def test_delete_network_unit(self):
        # Тест на удаление NetworkUnit
        url = f"/drf/api/NetworkUnit/{self.unit.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(NetworkUnit.objects.count(), 0)  # Проверяем, что запись была удалена


class TradingNetworkViewSetTests(APITestCase):
    def setUp(self):
        # Создаем пользователя и токен для авторизации
        self.user = Users(
            email="test@gmail.com",
            password="test",
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )
        self.user.set_password("test")
        self.user.save()

        self.client = APIClient()
        token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        self.trading_network = TradingNetwork.objects.create(title="Тестовая сеть")

    def test_list_trading_networks(self):
        # Тест на получение списка TradingNetwork
        url = "/drf/api/TradingNetwork/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Проверяем, что получили одну запись

    def test_create_trading_network(self):
        # Тест на создание TradingNetwork
        data = {
            "title": "Новая сеть",
        }
        url = "/drf/api/TradingNetwork/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TradingNetwork.objects.count(), 2)  # Проверяем, что количество записей увеличилось


class ProductViewSetTests(APITestCase):
    def setUp(self):
        # Создаем пользователя и токен для авторизации
        self.user = Users(
            email="test@gmail.com",
            password="test",
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )
        self.user.set_password("test")
        self.user.save()

        self.client = APIClient()
        token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        self.product = Product.objects.create(title="Тестовый продукт", model="Модель", release_date="2023-01-01")

    def test_list_products(self):
        # Тест на получение списка Product
        url = "/drf/api/Product/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Проверяем, что получили одну запись

    def test_create_product(self):
        # Тест на создание Product
        data = {
            "title": "Новый продукт",
            "model": "Новая модель",
            "release_date": "2023-02-01",
        }
        url = "/drf/api/Product/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)  # Проверяем, что количество записей увеличилось
