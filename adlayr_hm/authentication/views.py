from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.views import View
from healthmix.models import (
    BannerImage,
)
from .models import OTP, Profile
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

            # to send otp
            template = "email/otp_verification_mail.html"
            context = {
                'subject': f"{user.username}, Verify and Create Your New Account - OTP Inside 🐣🐥",
                'to_email': user.email,
                'OTP': otp,
            }
            send_email(template, context)

            user.save()

            request.session["email"] = user.email
            request.session["user_id"] = user.id
            return redirect('otp_verification')
        else:
            # to handle accounts already registered but not otp verified - now trying to verify otp
            # with same username & email
            username = request.POST.get("username")
            email = request.POST.get("email")
            users = Profile.objects.filter(username=username, email=email)
            user = users.first()

            if users.exists() and not user.is_email_verified:
                # generate and store new otp
                otp = generate_otp(user.email)

                # to send otp
                template = "email/otp_verification_mail.html"
                context = {
                    'subject': f"{user.username}, Verify and Create Your New Account - OTP Inside 🐣🐥",
                    'to_email': user.email,
                    'OTP': otp,
                }
                send_email(template, context)

                user.save()

                request.session["email"] = user.email
                request.session["user_id"] = user.id
                return redirect('otp_verification')


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
    
    def post(self,request,*args,**kwargs):
        user_email = request.session.get("email")
        user_id = request.session.get("user_id")
        otp = request.POST.get("otp", None)

        # otp verifiation
        otp_obj = OTP.objects.filter(email = user_email, is_verified = False).order_by('-created_at').first()
        if (
            check_password(otp, otp_obj.otp_hash) 
            and otp_obj.expires_at > timezone.now()
            and otp_obj.attempts <= 3
        ):
            otp_obj.attempts += 1
            otp_obj.is_verified = True
            otp_obj.save()
            user = Profile.objects.get(id=user_id)
            user.is_email_verified = True
            user.save()
            request.session["sign_up"] = True
            return redirect('login')
        else:
            if not check_password(otp, otp_obj.otp_hash):
                msg = "Invalid OTP..."
            if otp_obj.expires_at <= timezone.now():
                msg = f"OTP expired for email:{user_email}"
                otp_obj.delete()
            if otp_obj.attempts > 3:
                msg = "Invalid OTP, Maximum number attempt is reached"
            otp_obj.attempts += 1
            otp_obj.save()
            banner_image = BannerImage.objects.filter(is_active=True).first()
            data = {
                "banner_image": banner_image.image.url,
                'msg': msg if msg else None
            }

        return render(request, 'authentication/otp_verification.html', context=data)


    # ⭐ NEED IMPROVEMENTS
    # ✔️ Auto-submit when 6 digits filled
    # ✔️ Paste support (Ctrl + V)
    # ✔️ Countdown timer
    # ✔️ Resent OTP


class LoginViewset(View):
    form_class = LoginForm
    def get(self,request,*args,**kwargs):
        is_signup = request.session.get("sign_up", False)
        msg = False
        if is_signup:
            msg = 'Authenticated Successfully, Please Login'
        banner_image = BannerImage.objects.filter(is_active=True).first()
        form = self.form_class()
        data = {
            "banner_image": banner_image.image.url,
            'messages': msg,
            'form': form
        }
        return render(request, 'authentication/login.html', context=data)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)

            if user and user.is_email_verified == True:
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