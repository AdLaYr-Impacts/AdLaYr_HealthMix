from django.shortcuts import render, redirect
from decimal import Decimal
from django.views import View
from healthmix.models import (
    BannerImage,
    AnnouncementMessage,
    Product,
    ProductImage,
    Cart,
)

class HomeView(View):
    def get(self,request,*args,**kwargs):
        banner_image = BannerImage.objects.filter(is_active=True).first()
        announcement_message = AnnouncementMessage.objects.filter(is_active=True).order_by('-created_at').first()
        data = {
            "banner_image": banner_image.image.url,
            "announcement_message": announcement_message,
        }
        return render(request, 'adlayr_hm/home.html', context=data)
    

class ProductDetailsView(View):
    def get(self,request,slug,*args,**kwargs):
        product = Product.objects.filter(slug_field = slug).first()
        product_images = ProductImage.objects.filter(product = product).order_by("sort_order")
        data = {
            'product': product,
            'product_images': product_images,
        }
        return render(request,'adlayr_hm/product_details.html', context=data)
    
    def post(self,request,slug,*args,**kwargs):
        product = Product.objects.filter(slug_field = slug).first()
        product_images = ProductImage.objects.filter(product = product).order_by("sort_order")
        quantity = int(request.POST.get("quantity", 1))
        # if not request.user.is_authenticated:
        #     msg = "Please login to add items to cart"
        #     data = {
        #         'product': product,
        #         'product_images': product_images,
        #         "quantity": quantity,
        #         "msg": msg
        #     }
        #     return render(request,'adlayr_hm/product_details.html', context=data)

        price = Decimal(str(quantity))*(
            product.discounted_price 
            if product.discounted_price 
            else product.price
        )
        
        Cart.objects.create(
            user = request.user,
            product = product,
            quantity = quantity,
            price = price
        )
        return redirect('cart')
    

class CartView(View):
    def get(self,request,*args,**kwargs):
        cart_obj = Cart.objects.filter(user = request.user)
        product_image = ProductImage.objects.filter(
            product = cart_obj.first().product
        ).order_by("sort_order").first()
        data = {
            "cart_items": cart_obj,
            "image": product_image
        }
        return render(request,'adlayr_hm/cart.html', context=data)