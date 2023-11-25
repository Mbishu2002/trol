from django.urls import path
from .views import business_search

urlpatterns = [
    path('business_search/', business_search, name='business_search'),
]
