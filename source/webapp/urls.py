from webapp.views import ProductIndexView, ProductView, ProductCreateView, ProductDeleteView, \
    ProjectUpdateView, BasketCreateView, BasketIndexView, BasketDeleteView, OrderCreateView, \
    OrderList, OrderView
from django.urls import path

app_name = 'webapp'

urlpatterns = [
    path('', ProductIndexView.as_view(), name='index'),
    path('product/<int:pk>/', ProductView.as_view(), name='product_view'),
    path('product/add/', ProductCreateView.as_view(), name='create'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='delete'),
    path('product/<int:pk>/update', ProjectUpdateView.as_view(), name='update'),
    path('product/<int:pk>/basket', BasketCreateView.as_view(), name='basket_create'),
    path('product/basket', BasketIndexView.as_view(), name='basket_index'),
    path('basket/<int:pk>/delete', BasketDeleteView.as_view(), name='basket_delete'),
    path('order/create', OrderCreateView.as_view(), name='order_create'),
    path('order/list', OrderList.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderView.as_view(), name='order_view')
]