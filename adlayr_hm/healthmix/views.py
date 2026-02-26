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
    UserAddress,
    Order,
)
from .forms import UserAddressForm
from common.helper import generate_order_number

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
        if request.user.is_authenticated:
            cart_item_count = Cart.objects.filter(user = request.user).count()
        else:
            cart_item_count = 0
        data = {
            'product': product,
            'product_images': product_images,
            "cart_count": cart_item_count,
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
        user = request.user
        cart_obj = Cart.objects.filter(user = user)
        user_addres = UserAddress.objects.filter(user=user.id).first()
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
        if request.user.is_authenticated:
            cart_item_count = Cart.objects.filter(user = request.user).count()
        else:
            cart_item_count = 0
        data = {
            "cart_items": cart_obj,
            "image": product_image, 
            "total_price":total_price,
            "cart_count": cart_item_count,
            "user_addres": user_addres,
        }
        return render(request,'adlayr_hm/cart.html', context=data)
    

class CartUpdateView(View):
    def post(self,request,*args,**kwargs):
        cart_id = self.kwargs.get("id")
        quantity = request.POST.get("quantity")
        if cart_id:
            cart_item = Cart.objects.filter(id=cart_id).first()
            if cart_item:
                cart_item.quantity = quantity
                cart_item.save()
        return redirect("cart")
        

class CartDeleteView(View):
    def post(self, request, *args, **kwargs):
        cart_item_id = self.kwargs.get("id", None)
        if cart_item_id:
            cart_item = Cart.objects.filter(id=cart_item_id).first()
            if cart_item:
                cart_item.delete()
            return redirect("cart")
        

class UserProfileView(View):
    form_class = UserAddressForm
    def get(self, request, *args, **kwargs):
        user = request.user
        user_addres = UserAddress.objects.filter(user=user.id).first()
        form = self.form_class(instance=user_addres)
        if request.user.is_authenticated:
            cart_item_count = Cart.objects.filter(user = request.user).count()
        else:
            cart_item_count = 0
        data = {
            "user": user,
            "user_addres": user_addres,
            "form": form,
            "cart_count": cart_item_count,
        }
        return render(request, "adlayr_hm/user_profile.html", context=data)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        user_addres = UserAddress.objects.filter(user=user.id).first()
        form = self.form_class(request.POST, instance=user_addres)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = user
            form.save()
            return redirect('user_profile')
        
        data = {
            "user": user,
            "user_addres": user_addres,
            "form": form,
        }
        return render(request, "adlayr_hm/user_profile.html", context=data)
    

class ManageOrderViewset(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        cart_obj = Cart.objects.filter(user = user)
        user_addres = UserAddress.objects.filter(user=user.id).first()
        product = Product.objects.get(id=cart_obj.first().product.id)
        quantity = cart_obj.aggregate(total_quantity = Sum("quantity"))['total_quantity']
        price = quantity*(
            product.discounted_price if product.discounted_price
            else product.price
        )
        
        order = Order.objects.create(
            # order = generate_order_number(user),
            user = user,
            product = product,
            quantity = quantity,
            total_price = price,
            user_address = user_addres
        )
        order.order = f"ORD{order.id:07d}"
        order.save()

        return redirect("cart") # only for temporary