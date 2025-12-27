from django.contrib import admin

from .models import(
    Profile,
    OTP,
)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["username", "is_active", "role"]

class OTPAdmin(admin.ModelAdmin):
    list_display = ["email", "expires_at", "attempts", "is_verified"]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(OTP, OTPAdmin)