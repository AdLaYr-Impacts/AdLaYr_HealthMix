from django.shortcuts import render
from django.views import View
from healthmix.models import (
    BannerImage,
    AnnouncementMessage,
    Product,
    ProductImage,
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
    def get(self,request,*args,**kwargs):
        product_slug = request.kwargs.get("slug")
        product = Product.objects.filter(slug = product_slug)
        product_images = ProductImage.objects.filter(product = product).order_by("sort_order")
        data = {
            'product': product,
            'product_images': product_images,
        }
        return render(request,'adlayr_hm/product_details.html', context=data)