from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=8)
    profile_image = models.ImageField(upload_to="profile_pictures")
    is_business = models.BooleanField(default=False)
    about = models.TextField(null=True)

    def __str__(self):
        return self.name

class Category(models.TextChoices):
    FASHION = 'fashion', 'FASHION'
    FOOTWEAR = 'footwear', 'FOOTWEAR'
    CLOTHING = 'clothing', 'CLOTHING'
    SKINCARE = 'skincare', 'SKINCARE'
    ELECTRONICS = 'electronics', 'ELECTRONICS'
    MOBILE_PHONES = 'mobile_phones', 'MOBILE PHONES'
    OTHER = 'other', 'OTHER'

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('BusinessCategory', on_delete=models.CASCADE)

class BusinessCategory(models.Model):
    name = models.CharField(max_length=30, choices=Category.choices)
    businesses = models.ManyToManyField('Business')
    subcategories = models.ManyToManyField(SubCategory)

class Business(User):
    location = models.CharField(max_length=250)
    link = models.CharField(max_length=1000)
    categories = models.ManyToManyField(BusinessCategory)

class Social(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.CharField(max_length=1000)

class Followers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    business = models.ForeignKey(Business, related_name='followers', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower.name} follows {self.business.name}"

