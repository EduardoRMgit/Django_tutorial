from django.db import models


class CatalogoCodigosTEF(models.Model):
    rango = (
        ('00-19', 'ERROR DE CICS'),
        ('20-50', 'ERROR EN VALIDACION'),
        ('51-60', 'ERROR EN PAGO VENTANILLA'),
        ('61-  ', 'ERROR EN ARCHIVOS DEFINITIVOS')
    )
    etiqueta = models.CharField(max_length=64,
                                choices=rango,
                                null=False,
                                blank=False)
    codigo = models.CharField(max_length=2, blank=False, null=False)
    descripcion = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.descripcion
