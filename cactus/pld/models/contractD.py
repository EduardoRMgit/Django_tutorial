from django.db import models
from django.contrib.auth.models import User


class ContratoD(models.Model):
    """

    ``Attributes:``

    - Descripcion:

    - id_entidad = IntegerField(null=True)
    - curp = CharField(max_length=18)
    - rfc = CharField(max_length=15)
    - no_credito = CharField(max_length=20, blank=True, null=True)
    - unidad_credito = CharField(max_length=30, blank=True, null=True)
    - tipo_credito = CharField(max_length=30, blank=True, null=True)
    - tipo_moneda = CharField(max_length=20, blank=True, null=True)
    - T1 = FloatField(default=0, null=True)
    - T2 = FloatField(default=0, null=True)
    - T3 = DateField(null=True)  # fecha inical
    - T4 = DateField(null=True, blank=True)
    - instrumento_monetario = IntegerField(null=True)
    - canales_distribucion = CharField(max_length=30, blank=True,
                                            null=True)
    - Estado = CharField(max_length=30, blank=True, null=True)
    - status_code = CharField(max_length=3, blank=True, null=True)
    - mensaje = CharField(max_length=420, null=True)
    - user = many to one to user models


    """
    id_entidad = models.IntegerField(null=True)
    curp = models.CharField(max_length=18)  # LLaves UNIQUES
    rfc = models.CharField(max_length=15)  # LLaves UNIQUES
    no_credito = models.CharField(max_length=20, blank=True, null=True)
    unidad_credito = models.CharField(max_length=30, blank=True, null=True)
    tipo_credito = models.CharField(max_length=30, blank=True, null=True)
    tipo_moneda = models.CharField(max_length=20, blank=True, null=True)
    T1 = models.FloatField(default=0, null=True)  # total del contrato
    T2 = models.FloatField(default=0, null=True)  # cuota periodo determinado
    T3 = models.DateField(null=True)  # fecha inical
    T4 = models.DateField(null=True, blank=True)  # fecha final
    instrumento_monetario = models.IntegerField(null=True)  # tarjeta
    canales_distribucion = models.CharField(max_length=30, blank=True,
                                            null=True)  # donde
    Estado = models.CharField(max_length=30, blank=True, null=True)
    status_code = models.CharField(max_length=3, blank=True, null=True)
    mensaje = models.CharField(max_length=420, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='UDcontrato')

    def __str__(self):
        return self.no_credito

    class Meta():
        verbose_name_plural = 'UBcubo Contrato Default'
