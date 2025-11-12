from django.shortcuts import render, redirect
from django.views import View
from healthmix.models import (
    BannerImage,
)
from .forms import RegisterForm

class SignUpViewset(View):
    form_class = RegisterForm
    def get(self,request,*args,**kwargs):
        banner_image = BannerImage.objects.filter(is_active=True).first()
        form = self.form_class()
        data = {
            "banner_image": banner_image.image.url,
            "form": form,
        }
        return render(request, 'authentication/signup.html', context=data)

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        banner_image = BannerImage.objects.filter(is_active=True).first()
        data = {
            "banner_image": banner_image.image.url,
            'form': form
        }
        return render(request, 'authentication/signup.html', context=data)

class OtpVerificationViewset(View):
    def get(self,request,*args,**kwargs):
        banner_image = BannerImage.objects.filter(is_active=True).first()
        data = {
            "banner_image": banner_image.image.url,
        }
        return render(request, 'authentication/otp_verification.html', context=data)


class LoginViewset(View):
    def get(self,request,*args,**kwargs):
        banner_image = BannerImage.objects.filter(is_active=True).first()
        data = {
            "banner_image": banner_image.image.url,
        }
        return render(request, 'authentication/login.html', context=data)


class LogoutViewset(View):
    def get(self,request,*args,**kwargs):
        pass