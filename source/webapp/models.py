from django.core.validators import MinValueValidator
from django.db import models

DEFAULT_CATEGORY = 'other'

CATEGORY_CHOICES = [
    (DEFAULT_CATEGORY, 'Разное'),
    ('food', 'Еда'),
    ('clothes', 'Одежда'),
    ('car', 'Для машины'),
    ('wash', 'Чистящие средства'),
    ('tools', 'Инструменты'),
    ('toys', 'Игрушки')
]


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Название')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, null=False, blank=False,
                                default=DEFAULT_CATEGORY, verbose_name='Категория')
    amount = models.IntegerField(verbose_name='Остаток', validators=[(MinValueValidator(0))])

    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2)

    def __str__(self):
        return f'{self.name} - {self.amount}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Basket(models.Model):
    products = models.ForeignKey('webapp.Product', related_name='products_basket', on_delete=models.PROTECT,
                               verbose_name='Товары')
    amount = models.IntegerField(verbose_name='Остаток')

    def __str__(self):
        return f'{self.pk} - {self.products}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Order(models.Model):
    user_name = models.CharField(max_length=100, blank=False, null=False, verbose_name='Имя пользователя')
    phone = models.CharField(max_length=150, blank=False, null=False, verbose_name='Телефон')
    address = models.CharField(max_length=400, blank=False, null=False, verbose_name='Адрес')
    date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField('webapp.Product', related_name='orders', through='webapp.ProductOrder',
                                      through_fields=('order', 'product', 'product_amount'), blank=True,
                                      verbose_name='Продукты')


class ProductOrder(models.Model):
    product = models.ForeignKey('webapp.Product', related_name='product_order', on_delete=models.CASCADE)
    order = models.ForeignKey('webapp.Order', related_name='order_product', on_delete=models.CASCADE)
    products_amount = models.IntegerField(verbose_name='Колличество')
