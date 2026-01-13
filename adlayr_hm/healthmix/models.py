from django.db import models
from django.conf import settings
import uuid

# Common Model
class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# model to handle banner image
class BannerImage(BaseModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/')
    button_text = models.CharField(max_length=255, blank=True, null=True)
    button_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

# model to handle product
class Product(BaseModel):
    name = models.CharField(max_length=255)
    slug_field = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    nutrition_info = models.TextField(blank=True, null=True)
    ingredients = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"product: {self.name}"

# model to handle product variation categorey
class ProductVariationCategorey(BaseModel):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    categorey = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.Product.name} - {self.categorey}"

# model to handle product variation
class ProductVariation(BaseModel):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    categorey = models.ForeignKey(ProductVariationCategorey, on_delete=models.CASCADE)
    tier_variation = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.Product.name} - {self.categorey.categorey} - {self.tier_variation}"

# model to manage inventory
class Inventory(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"product: {self.product.name} stock: {self.stock}"

# model to keep product images
class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=255, null=True, blank=True)
    sort_order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} image"

# model to manage order
class Order(BaseModel):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    weight_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE) # need update
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    user_address = models.ForeignKey("UserAddress", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.order} {self.user.username} {self.product.name} {self.quantity}"

# model to store rating and reviews
class RatingAndReview(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_rating")
    rating = models.PositiveIntegerField(default=0)
    review = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=True)
    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.rating}/5"

# model to keep user address
class UserAddress(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_address")
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=50, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"

# model for user's questions
class FAQQuestions(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_questions")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    question = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.question} by {self.user.firstname}"

# model to keep admin's answers for user's questions
class FAQAnswers(BaseModel):
    question = models.ForeignKey(FAQQuestions, on_delete=models.CASCADE)
    answer = models.TextField()

# model to keep announcement or sales message
class AnnouncementMessage(BaseModel):
    message = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.message
    

# model to handle product detail banner image
class ProductDetailBannerImage(BaseModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/')
    button_text = models.CharField(max_length=255, blank=True, null=True)
    button_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"