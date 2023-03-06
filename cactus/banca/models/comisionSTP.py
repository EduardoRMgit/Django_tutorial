from django.db import models


class ComisioneSTP(models.Model):
    stp = models.FloatField()
    ivaSTP = models.FloatField()
    cliente = models.FloatField()
    ivaCliente = models.FloatField()

    def __str__(self):
        return "cliente: " + str(self.cliente)
