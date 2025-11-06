from django.shortcuts import render
from django.views import View
from healthmix.models import (
    BannerImage,
    AnnouncementMessage,
)

class HomeView(View):
    def get(self,request,*args,**kwargs):
        banner_image = BannerImage.objects.filter(is_active=True).first()
        announcement_message = AnnouncementMessage.objects.filter(is_active=True).first()
        data = {
            "banner_image": banner_image.image.url,
            "announcement_message": announcement_message,
        }
        return render(request, 'adlayr_hm/home.html', context=data)

class SignUpViewset(View):
    def get(self,request,*args,**kwargs):
        banner_image = BannerImage.objects.filter(is_active=True).first()
        data = {
            "banner_image": banner_image.image.url,
        }
        return render(request, 'adlayr_hm/signup.html', context=data)

class OtpVerificationViewset(View):
    def get(self,request,*args,**kwargs):
        banner_image = BannerImage.objects.filter(is_active=True).first()
        data = {
            "banner_image": banner_image.image.url,
        }
        return render(request, 'adlayr_hm/otp_verification.html', context=data)


class LoginViewset(View):
    def get(self,request,*args,**kwargs):
        banner_image = BannerImage.objects.filter(is_active=True).first()
        data = {
            "banner_image": banner_image.image.url,
        }
        return render(request, 'adlayr_hm/login.html', context=data)