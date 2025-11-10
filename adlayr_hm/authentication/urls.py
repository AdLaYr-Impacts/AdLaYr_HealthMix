from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpViewset.as_view(), name='signup'),
    path('signup/otp_verification/', views.OtpVerificationViewset.as_view(), name='otp_verification'),
    path('login/', views.LoginViewset.as_view(), name='login'),
    path('logout/', views.LogoutViewset.as_view(), name='logout'),
]