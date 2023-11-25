# search/views.py
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Profile.models import Business
from Profile.serializers import BusinessSerializer
from .models import Search
from .serializers import SearchSerializer
from typing import Dict

@api_view(['GET'])
def business_search(request):
    query = request.query_params.get('query', '')
    location = request.query_params.get('location', '')
    category = request.query_params.get('category', '')

    search_query = Q(name__icontains=query) | Q(bio__icontains=query)  

    if location:
        search_query &= Q(location__icontains=location)

    if category:
        search_query &= Q(categories__name=category)

    businesses = Business.objects.filter(search_query)
    
    
    user = request.user if request.user.is_authenticated else None
    search_data = request.data
    search_serializer = SearchSerializer(data=search_data)
    if search_serializer.is_valid():
        search_serializer.save()

    
    serializer = BusinessSerializer(businesses, many=True, context={'request': request})
    return Response(serializer.data)
