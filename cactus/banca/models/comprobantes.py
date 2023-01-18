from django.db import models


class Comprobante(models.Model):

    class Meta():
        verbose_name = 'Template de Comprobante'
        verbose_name_plural = 'Templates de Comprobantes'

    tipo = models.CharField(max_length=80)
    codigo = models.IntegerField(unique=True)
    template = models.ImageField(
        upload_to='docs/plantillas',
        blank=False,
        null=False
    )

    def __str__(self):
        return self.tipo
