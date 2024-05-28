from rest_framework import serializers
from .models import Comanda
from carreto.models import CarretoProduct

class ComandaSerializer(serializers.ModelSerializer):
    total_products = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    class Meta:
        model = Comanda
        fields = '__all__'

    def get_total_products(self, obj):
        return CarretoProduct.objects.filter(carreto=obj.carreto).count()

    def get_total_price(self, obj):
        products = CarretoProduct.objects.filter(carreto=obj.carreto)
        return sum(product.quantitat * product.preu for product in products)

    def get_products(self, obj):
        products = CarretoProduct.objects.filter(carreto=obj.carreto)
        return [{"product_id": p.product.id, "name": p.product.name, "quantity": p.quantitat, "price": p.preu} for p in products]