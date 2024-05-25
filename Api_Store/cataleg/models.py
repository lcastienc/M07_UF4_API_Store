from django.db import models

# Create your models here.

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField()
    fabrication = models.CharField(max_length=100)
    OriginCountry = models.CharField(max_length=100)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.name} {self.price} {self.description} {self.stock} {self.fabrication} {self.OriginCountry} {self.deleted} {self.created_at} {self.updated_at}'
