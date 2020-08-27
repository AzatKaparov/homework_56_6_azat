from django.contrib import admin
from django.urls import path
from webapp.views import index_view, product_view, create_view, delete_view, update_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('product/<int:pk>/', product_view, name='product_view'),
    path('product/add/', create_view, name='create'),
    path('product/<int:pk>/delete', delete_view, name='delete'),
    path('product/<int:pk>/update', update_view, name='update'),
]
