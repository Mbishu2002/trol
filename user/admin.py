from django.contrib import admin
from .models import User, Social, Business, BusinessCategory, SubCategory

admin.site.register(User)
admin.site.register(Social)
admin.site.register(Business)
admin.site.register(BusinessCategory)
admin.site.register(SubCategory)
