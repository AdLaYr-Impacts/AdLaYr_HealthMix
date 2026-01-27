from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product_details/<slug:slug>/', views.ProductDetailsView.as_view(), name='product_details'),
    path('cart/', views.CartView.as_view(), name='cart'),
]