from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from webapp.models import Product, Basket
from webapp.forms import SimpleSearchForm, OrderForm
from django.utils.http import urlencode
from django.views.generic import ListView, DeleteView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


class BasketCreateView(View):
    model = Basket
    form_class = None
    queryset = Basket.objects.all()

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        try:
            basket = Basket.objects.get(products=product, session_id=self.get_session_key())
            basket.amount += 1
            basket.save()
            messages.add_message(self.request, messages.SUCCESS, f'Добавлен товар: {basket.products.name}')
        except ObjectDoesNotExist:
            if product.amount <= 0:
                messages.add_message(self.request, messages.ERROR, f'Товара не осталось в наличии')
                return redirect('index')
            else:
                basket = Basket.objects.create(products=product, amount=1, session_id=self.get_session_key())
                messages.add_message(self.request, messages.SUCCESS, f'Добавлен товар: {basket.products.name}')
        return redirect('webapp:index')

    def get_session_key(self):
        session = self.request.session
        if not session.session_key:
            session.save()
        return session.session_key


class BasketIndexView(ListView):
    template_name = 'basket/basket_index.html'
    context_object_name = 'baskets'
    model = Basket
    queryset = Basket.objects.all()

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['all'] = 0
        for i in Basket.objects.all():
            context['all'] += (i.products.price * i.amount)
        baskets = []
        for i in Basket.objects.all():
            baskets.append({'total': i.products.price * i.amount, 'product': i.products, 'amount': i.amount, 'pk': i.pk})
        context['ford'] = self.form
        context['baskets'] = baskets
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        context['form'] = OrderForm(data=self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(id__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset.filter(session_id=self.get_session_key())

    def get_session_key(self):
        session = self.request.session
        if not session.session_key:
            session.save()
        return session.session_key

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class BasketDeleteView(DeleteView):
    model = Basket
    template_name = 'basket/basket_delete.html'
    success_url = reverse_lazy('webapp:basket_index')

    def get_context_data(self, **kwargs):
        super().get_context_data()
        messages.add_message(self.request, messages.WARNING, f'Вы собираетесь удалить этот товар из корзины!')
