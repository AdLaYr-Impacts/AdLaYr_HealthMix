from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from healthmix.models import (
    BannerImage,
)
from .forms import (
    RegisterForm,
    LoginForm
)
from common.helper import send_email, generate_otp

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
            user = form.save(commit=False)
            user.role = 'User'

            # generate and store otp
            otp = generate_otp(user.email)

            # otp verification
            template = "email/otp_verification_mail.html"
            context = {
                'subject': f"{user.username}, Verify and Create Your New Account - OTP Inside 🐣🐥",
                'to_email': user.email,
                'OTP': otp,
            }
            send_email(template, context)

            user.save()
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
    form_class = LoginForm
    def get(self,request,*args,**kwargs):
        banner_image = BannerImage.objects.filter(is_active=True).first()
        form = self.form_class()
        data = {
            "banner_image": banner_image.image.url,
            'form': form
        }
        return render(request, 'authentication/login.html', context=data)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)

            if user:
                login(request, user)
                return redirect('home')
            
            msg = 'Invalid Credentials'
        banner_image = BannerImage.objects.filter(is_active=True).first()
        data = {
            'form': form,
            'msg': msg if 'msg' in locals() else None,
            "banner_image": banner_image.image.url,
        }
        return render(request, 'authentication/login.html', context=data)

class LogoutViewset(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('home')