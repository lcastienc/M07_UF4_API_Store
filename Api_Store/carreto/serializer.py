from rest_framework import serializers
from .models import Carreto,CarretoProduct

class CarretoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carreto
        fields = ['id', 'client', 'preu_total', 'finalitzat', 'created_at', 'updated_at']

class CarretoProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarretoProduct
        fields = ['id', 'carreto', 'product', 'quantitat', 'preu']