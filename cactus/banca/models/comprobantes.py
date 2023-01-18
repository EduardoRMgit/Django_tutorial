from django.db import models
from banca.models import TipoTransaccion


class Comprobante(models.Model):

    class Meta():
        verbose_name = 'Template de Comprobante'
        verbose_name_plural = 'Templates de Comprobantes'

    tipo = models.ForeignKey(
        TipoTransaccion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    codigo = models.IntegerField(unique=True)
    template = models.ImageField(
        upload_to='docs/plantillas',
        blank=False,
        null=False
    )

    def __str__(self):
        return self.tipo
