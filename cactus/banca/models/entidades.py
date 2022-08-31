from django.db import models


class CodigoConfianza(models.Model):

    nombre = models.CharField(max_length=200)
    codigo_referencia = models.CharField(max_length=16)

    class Meta():
        verbose_name_plural = 'Codigos de confianza'

    def __str__(self):
        return self.nombre
