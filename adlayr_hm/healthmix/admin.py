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
)

admin.site.register(BannerImage)
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