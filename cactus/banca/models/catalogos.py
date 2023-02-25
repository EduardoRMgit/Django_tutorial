from django.db import models


class ErroresTransaccion(models.Model):
    codigo = models.CharField(max_length=6)
    mensaje = models.CharField(max_length=128)
    codigo_ext = models.CharField(max_length=4)
    mensaje_ext = models.CharField(max_length=128)

    class Meta():
        verbose_name_plural = 'Errores de Transacción'

    def __str__(self):
        return self.mensaje


class TipoTransaccion(models.Model):
    TIPO = (
        ('E', 'Enviada'),
        ('R', 'Recibida'),
        ('S', 'Especial')
    )
    MEDIO = (
        ('E', 'Efectivo'),
        ('T', 'Transferencia')
    )
    codigo = models.CharField(max_length=3)
    nombre = models.CharField(max_length=128)
    tipo = models.CharField(
        max_length=1,
        choices=TIPO,
        null=True,
        blank=True)
    medio = models.CharField(
        max_length=1,
        choices=MEDIO,
        null=True,
        blank=True)
    salida = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta():
        verbose_name_plural = 'Tipos de Transaccion'


class Comision(models.Model):
    monto = models.FloatField()
    descripcion = models.CharField(max_length=16)
    tipo = models.ForeignKey(
        TipoTransaccion,
        on_delete=models.CASCADE,
        related_name='tipo_comision'
    )

    def __str__(self):
        return self.descripcion

    class Meta():
        verbose_name_plural = 'Comisiones'


class CAMI(models.Model):
    """
    Catalogo alertas monto inusual
    """
    DIA = 0
    MES = 1

    TIPO_CHOICES = (
        (DIA, "Diaria"),
        (MES, "Mensual")
    )

    nombre = models.CharField(max_length=128, blank=True, null=True)
    monto = models.FloatField()
    unidad = models.CharField(max_length=10, blank=True, null=True)
    pesos = models.FloatField()
    tipo = models.IntegerField(choices=TIPO_CHOICES, default=DIA)

    def __str__(self):
        return self.nombre
