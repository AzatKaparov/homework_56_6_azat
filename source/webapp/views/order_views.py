from django.shortcuts import redirect
from django.views.generic import View, ListView, DetailView
from webapp.models import Order, Basket, ProductOrder, Product
from webapp.forms import OrderForm


class OrderCreateView(View):
    def post(self, request, *args, **kwargs):
        form = OrderForm(data=request.POST)
        if form.is_valid():
            if self.request.user.is_authenticated:
                order = Order.objects.create(
                    user_name=form.cleaned_data['user_name'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                    user=self.request.user)
            else:
                order = Order.objects.create(
                    user_name=form.cleaned_data['user_name'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                    user=None)

            for i in Basket.objects.all():
                product = Product.objects.get(pk=i.products.pk)
                product.amount = (i.products.amount - i.amount)
                product.save()
                ProductOrder.objects.create(products_amount=i.amount,
                                            order_id=order.pk, product_id=i.products.pk)
        Basket.objects.all().delete()

        return redirect('webapp:index')


class OrderList(ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset


class OrderView(DetailView):
    model = Order
    template_name = 'order/order_view.html'
    context_object_name = 'order'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        print(self.object.products.all())
        return context



