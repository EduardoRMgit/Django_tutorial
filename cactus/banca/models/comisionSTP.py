from django.db import models


class ComisioneSTP(models.Model):
    stp = models.FloatField()
    ivaSTP = models.FloatField()
    cliente = models.FloatField()
    ivaCliente = models.FloatField()
    rangotransacciones = models.CharField(
        max_length=256, blank=True, null=True)

    def __str__(self):
        return "cliente: " + str(self.cliente)
