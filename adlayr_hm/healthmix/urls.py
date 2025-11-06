from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('signup/', views.SignUpViewset.as_view(), name='signup'),
    path('signup/otp_verification/', views.OtpVerificationViewset.as_view(), name='otp_verification'),
    path('login/', views.LoginViewset.as_view(), name='login'),
]