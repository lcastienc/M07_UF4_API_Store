from django.db import models
from client.models import Client
from carreto.models import Carreto

# Create your models here.

class Comanda(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    carreto = models.ForeignKey(Carreto, on_delete=models.CASCADE)
    estat = models.CharField(max_length=20, default='Obert')
    data_comanda = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.client} - {self.carreto} - {self.estat} - {self.data_comanda} - {self.created_at} - {self.updated_at}'
