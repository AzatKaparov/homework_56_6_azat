from django.contrib import admin
from .models import Product, Basket


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'amount', 'price')
    fields = ['name', 'category', 'amount', 'price', 'description', 'img']
    search_fields = ('name',)
    list_filter = ('category',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Basket)
