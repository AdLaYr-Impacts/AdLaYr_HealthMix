from django.shortcuts import render, redirect
from decimal import Decimal
from django.db.models import (
    Sum, 
    F, 
    Case, 
    When, 
    DecimalField
)
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
        if request.user.is_authenticated:
            cart_item_count = Cart.objects.filter(user = request.user).count()
        else:
            cart_item_count = 0
        data = {
            "banner_image": banner_image.image.url,
            "announcement_message": announcement_message,
            "cart_count": cart_item_count,
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

        print(quantity)

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
        total_price = cart_obj.aggregate(total = Sum(
            F('quantity')*
            Case(
                When(product__discounted_price__isnull=False,
                    then=F('product__discounted_price')),
                default=F('product__price'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        ))['total'] or 0
        product_image = None
        if cart_obj.exists():
            product_image = ProductImage.objects.filter(
                product = cart_obj.first().product
            ).order_by("sort_order").first()
        data = {
            "cart_items": cart_obj,
            "image": product_image,
            "total_price":total_price,
        }
        return render(request,'adlayr_hm/cart.html', context=data)