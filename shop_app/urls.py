from django.urls import path
from .views import products
from . import views

urlpatterns = [
    path('products', views.products, name='products'),
]
