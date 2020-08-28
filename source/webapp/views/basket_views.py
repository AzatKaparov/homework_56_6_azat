from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from webapp.models import Product, Basket
from django.http import HttpResponseNotAllowed
from webapp.forms import ProductForm, SimpleSearchForm, BasketForm
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View
from django.core.exceptions import ObjectDoesNotExist


class BasketCreateView(View):
    model = Basket
    form_class = BasketForm
    queryset = Basket.objects.all()

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        try:
            basket = Basket.objects.get(products=product)
            basket.amount += 1
            basket.save()
        except ObjectDoesNotExist:
            if product.amount == 0:
                return redirect('index')
            else:
                Basket.objects.create(products=product, amount=1)
        return redirect('index')


class BaskletIndexView(ListView):
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
        context['form'] = self.form
        context['baskets'] = baskets
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(id__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class BasketDeleteView(DeleteView):
    model = Basket
    template_name = 'basket/basket_delete.html'
    success_url = reverse_lazy('basket_index')
