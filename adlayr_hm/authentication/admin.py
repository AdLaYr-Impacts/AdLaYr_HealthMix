from django.contrib import admin

from .models import(
    Profile,
)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["username", "is_active", "role"]

admin.site.register(Profile, ProfileAdmin)