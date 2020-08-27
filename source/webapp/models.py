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
