from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import Product
from django.http import HttpResponseNotFound, HttpResponseNotAllowed
from .forms import ProductForm


def index_view(request):
    data = Product.objects.all().order_by('category', 'name')
    above_zero = []
    for i in data:
        if i.amount > 1:
            above_zero.append(i)
        else:
            pass
    return render(request, 'index.html', context={
        'products': above_zero
    })


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'product_view.html', context)


def delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        return render(request, 'delete.html', context={'product': product})
    elif request.method == 'POST':
        product.delete()
        return redirect('index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "GET":
        form = ProductForm(initial={
            'name': product.name,
            'description': product.description,
            'category': product.category,
            'amount': product.amount,
            'price': product.price,
            'img': product.img
        })
        return render(request, 'update.html', context={
            'form': form,
            'product': product
        })
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.description = form.cleaned_data['description']
            product.category = form.cleaned_data['category']
            product.amount = form.cleaned_data['amount']
            product.price = form.cleaned_data['price']
            product.img = form.cleaned_data['img']
            product.save()
            return redirect('product_view', pk=product.pk)
        else:
            return render(request, 'update.html', context={
                'product': product,
                'form': form,
                'errors': form.errors
            })
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def create_view(request, *args, **kwargs):
    if request.method == "GET":
        form = ProductForm()
        return render(request, 'create.html', context={
            'form': form
        })
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product = Product.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                category=form.cleaned_data['category'],
                price=form.cleaned_data['price'],
                amount=form.cleaned_data['amount'],
                img=form.cleaned_data['img'],
            )
        else:
            return render(request, 'create.html', context={
                'form': form
            })

        return redirect('product_view', pk=product.pk)