from django.core.exceptions import ValidationError
from django.db import models

class TradingNetwork(models.Model):
    """Модель, представляющая торговую сеть."""
    title = models.CharField(max_length=200, verbose_name='Название торговой сети')

    class Meta:
        verbose_name = "Торговая сеть"
        verbose_name_plural = "Торговые сети"

    def __str__(self):
        return self.title

class Product(models.Model):
    """Модель, представляющая продукт."""
    title = models.CharField(verbose_name='Название продукта', max_length=100)
    model = models.CharField(verbose_name='Модель продукта', max_length=100)
    release_date = models.DateField(verbose_name='Дата выпуска на рынок')

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.title

class NetworkUnit(models.Model):
    """Модель, представляющая поставщика."""
    LEVEL_CHOICES = [
        (0, 'Завод'),
        (1, 'Розничная сеть'),
        (2, 'Индивидуальный предприниматель')
    ]

    level = models.PositiveSmallIntegerField(verbose_name='Тип поставщика', choices=LEVEL_CHOICES, default=0)
    name = models.CharField(verbose_name='Название поставщика', max_length=100, unique=True)
    email = models.EmailField(verbose_name='Email поставщика', max_length=100, unique=True, null=True, blank=True)
    country = models.CharField(verbose_name='Страна', max_length=100)
    city = models.CharField(verbose_name='Город', max_length=100)
    street = models.CharField(verbose_name='Улица', max_length=100)
    house_number = models.CharField(verbose_name='Номер дома', max_length=10)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    debt_to_supplier = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Задолженность перед поставщиком',
        null=True, blank=True,
        default=0)
    trading_network = models.ForeignKey(
        TradingNetwork,
        verbose_name="Торговая сеть",
        on_delete=models.CASCADE)
    provider = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        verbose_name='Подрядчик',
        null=True,
        blank=True)
    products = models.ManyToManyField(Product, verbose_name='Продукты')

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    def __str__(self):
        return self.name

    def clean(self):
        if self.provider:
            if self.provider == self:
                raise ValidationError("Поставщик не может быть подрядчиком для самого себя.")
            if self.provider.level == self.level:
                raise ValidationError("Подрядчик не может быть на том же уровне иерархии.")
            if self.provider.level > self.level:
                raise ValidationError("Подрядчик должен быть на более высоком уровне иерархии.")
