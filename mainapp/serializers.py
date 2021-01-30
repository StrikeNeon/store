# -*- coding: utf-8 -*-

from .models import Brand, Merch, Review, Order
from rest_framework import serializers

class MerchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Merch
        fields = ['ID', 'Name', 'Usage', 'brand','Price','Description','PublishDate']

class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ['ID', 'Brandname', 'Country']

class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = ['ID', 'user_id', 'product', 'review_text','rating']
        
class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['order', 'product', 'price', 'quantity']