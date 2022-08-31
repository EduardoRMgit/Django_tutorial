from django.db import models
from banca.models.transaccion import Transaccion


class ComisioneSTP(models.Model):
    stp = models.FloatField()
    ivaSTP = models.FloatField()
    cliente = models.FloatField()
    ivaCliente = models.FloatField()
    transaccion = models.OneToOneField(Transaccion,
                                       on_delete=models.CASCADE,
                                       blank=True,
                                       null=True)

    def __str__(self):
        return "cliente: " + str(self.cliente)
