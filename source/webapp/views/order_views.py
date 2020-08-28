from django.shortcuts import redirect
from django.views.generic import View
from webapp.models import Order, Basket, ProductOrder, Product
from webapp.forms import OrderForm


class OrderCreateView(View):
    def post(self, request, *args, **kwargs):
        form = OrderForm(data=request.POST)
        if form.is_valid():
            order = Order.objects.create(user_name=form.cleaned_data['user_name'],
                                         phone=form.cleaned_data['phone'],
                                         address=form.cleaned_data['address'])

            for i in Basket.objects.all():
                product = Product.objects.get(pk=i.products.pk)
                product.amount = (i.products.amount - i.amount)
                product.save()
                ProductOrder.objects.create(products_amount=i.amount,
                                            order_id=order.pk, product_id=i.products.pk)
        Basket.objects.all().delete()

        return redirect('index')