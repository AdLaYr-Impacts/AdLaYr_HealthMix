from django.contrib import admin

from .models import(
    BannerImage,
    Product,
    ProductVariationCategorey,
    ProductVariation,
    Inventory,
    ProductImage,
    Order,
    RatingAndReview,
    UserAddress,
    FAQQuestions,
    FAQAnswers,
    AnnouncementMessage,
)

class BannerImageAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "created_at"]

class AnnouncementMessageAdmin(admin.ModelAdmin):
    list_display = ["message", "is_active"]

admin.site.register(BannerImage, BannerImageAdmin)
admin.site.register(Product)
admin.site.register(ProductVariationCategorey)
admin.site.register(ProductVariation)
admin.site.register(Inventory)
admin.site.register(ProductImage)
admin.site.register(Order)
admin.site.register(RatingAndReview)
admin.site.register(UserAddress)
admin.site.register(FAQQuestions)
admin.site.register(FAQAnswers)
admin.site.register(AnnouncementMessage, AnnouncementMessageAdmin)