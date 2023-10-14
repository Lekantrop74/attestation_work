from django.contrib import admin
from django.utils.html import format_html
from electronic_shop.models import *


@admin.register(Product)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(TradingNetwork)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(NetworkUnit)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", 'provider_url', 'level', 'city']
    list_filter = ('city',)
    actions = ['clear_arrears']

    def provider_url(self, obj):
        if obj.provider:
            return format_html("<a href='{url}'>{name}</a>", url=obj.provider.id, name=obj.provider.name)
        return "N/A"

    provider_url.short_description = "Ссылка на подрядчика"

    @admin.action(description='Очистить задолженность перед поставщиком')
    def clear_arrears(self, request, queryset) -> None:
        """ Clear arrears of unit """
        queryset.update(debt_to_supplier=0)
