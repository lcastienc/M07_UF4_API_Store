from django.db import models
from cataleg.models import Product
from client.models import Client

# Create your models here.

class Carreto(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    #especifico el valor del precion del carrito como 0
    preu_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    finalitzat = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} {self.client} {self.preu_total} {self.finalitzat} {self.created_at} {self.updated_at}'


class CarretoProduct(models.Model):
    id = models.AutoField(primary_key=True)
    carreto = models.ForeignKey(Carreto, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantitat = models.PositiveIntegerField(default=1)
    preu = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return f'{self.id} {self.carreto} {self.product} {self.quantitat} {self.price}'