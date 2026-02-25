from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product_details/<slug:slug>/', views.ProductDetailsView.as_view(), name='product_details'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/update/<int:id>/', views.CartUpdateView.as_view(), name='cart_item_update'),
    path('cart/remove/<int:id>/', views.CartDeleteView.as_view(), name='cart_item_delete'),
    path('user-profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('checkout/', views.ManageOrderViewset.as_view(), name="manage_order")
]