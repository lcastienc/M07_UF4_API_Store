from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description', 'stock', 'fabrication', 'OriginCountry', 'deleted', 'created_at', 'updated_at')
