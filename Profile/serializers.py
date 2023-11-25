from rest_framework import serializers
from .models import User, Social, Business, BusinessCategory, SubCategory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = '__all__'

class BusinessSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=BusinessCategory.objects.all())

    class Meta:
        model = Business
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class BusinessCategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = BusinessCategory
        fields = '__all__'
class SetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'password',
            'token',
            'uidb64'
        ]
class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = '__all__'