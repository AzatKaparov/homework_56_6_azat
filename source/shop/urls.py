from django.contrib import admin
from django.urls import path
from webapp.views import ProductIndexView, ProductView, ProductCreateView, ProductDeleteView, ProjectUpdateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ProductIndexView.as_view(), name='index'),
    path('product/<int:pk>/', ProductView.as_view(), name='product_view'),
    path('product/add/', ProductCreateView.as_view(), name='create'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='delete'),
    path('product/<int:pk>/update', ProjectUpdateView.as_view(), name='update'),
]
