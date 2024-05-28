from django.db import models
from comandes.models import Comanda

# Create your models here.

class Pagament(models.Model):
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    data_expiration = models.CharField(max_length=7)
    cvc = models.CharField(max_length=3)

    def __str__(self):
        return f'{self.comanda} {self.card_number} {self.data_expiration} {self.cvc}'