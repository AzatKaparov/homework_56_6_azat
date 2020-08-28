from django import forms
from django.core.validators import MinValueValidator

from .models import CATEGORY_CHOICES, DEFAULT_CATEGORY, Product, Basket


class ProductForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, label='Название')
    description = forms.CharField(required=False, label='Описание', widget=forms.Textarea)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=True, label='Категория',
                               initial=DEFAULT_CATEGORY)
    amount = forms.IntegerField(label='Остаток', validators=[(MinValueValidator(0))])
    price = forms.DecimalField(label='Цена', max_digits=7, decimal_places=2)

    class Meta:
        model = Product
        exclude = []


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")


class BasketForm(forms.ModelForm):

    class Meta:
        model = Basket
        exclude = []
