from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id','username','password')
        extra_kwargs = {'password':{'write_only':True}}
    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    def get__id(self,obj):
        return obj.id

    def get_isAdmin(self,obj):
        return obj.is_staff

    def get_name(self,obj):
        name = obj.first_name
        if name=="":
            name = obj.email
        return name

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at', 'updated_at','image']
class ReviewSerializer(serializers.ModelSerializer):
    reviewerName = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = ['id', 'product', 'rating', 'comment', 'date', 'reviewerName']

    def get_reviewerName(self, obj):
        return obj.reviewer.username 
class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only= True)
    class Meta:
        model = Product 
        fields = '__all__'
    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data