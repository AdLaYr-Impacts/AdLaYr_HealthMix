from django.shortcuts import render
from django.views import View
from healthmix.models import (
    BannerImage
)

class HomeView(View):
    def get(self,request,*args,**kwargs):
        banner_image = BannerImage.objects.filter(is_active=True).first()
        data = {
            "banner_image": banner_image.image.url
        }
        return render(request, 'adlayr_hm/home.html', context=data)