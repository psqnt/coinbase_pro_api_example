from django.contrib import admin

from .models import Currency, Product, ProductStatistics


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name',)
    list_filter = ('symbol', 'name',)
    ordering = ['-symbol']


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id',
                    'base_currency',
                    'quote_currency',
                    'display_name',)
    list_filter = ('product_id',
                   'base_currency',
                   'quote_currency',
                   'display_name',)
    ordering = ['-product_id']


class ProductStatisticsAdmin(admin.ModelAdmin):
    list_display = ('product', 'open', 'high', 'low',
                    'volume', 'last', 'volume_30day','last_updated',)
    list_filter = ('product', 'open', 'high', 'low',
                    'volume', 'last', 'volume_30day','last_updated',)
    ordering = ['-last_updated']


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductStatistics, ProductStatisticsAdmin)
