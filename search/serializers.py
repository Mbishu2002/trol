# search/serializers.py
from rest_framework import serializers
from Profile.serializers import BusinessSerializer
from .models import Search

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'
