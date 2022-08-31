from django.db import models
from .customer import Customer
from django.contrib.auth.models import User


class Contrato(models.Model):

    """

    ``Attributes:``

    - Descripcion:

    - id_entidad = IntegerField(null=True)
    - curp = CharField(max_length=18)
    - rfc = models.CharField(max_length=15)
    - no_credito = CharField(max_length=20, blank=True, null=True)
    - unidad_credito = CharField(max_length=30, blank=True, null=True)
    - tipo_moneda = CharField(max_length=20, blank=True, null=True)
    - T1 = FloatField(default=0, null=True)
    - T2 = FloatField(default=0, null=True)
    - T3 = DateField(null=True)
    - instrumento_monetario = IntegerField(null=True)
    - canales_distribucion = CharField(max_length=30, blank=True,
                                            null=True)
    - Estado = CharField(max_length=30, blank=True, null=True)
    - status_code = CharField(max_length=3, blank=True, null=True)
    - mensaje = CharField(max_length=420, null=True, blank=True)
    - user = many to one to user models
    - customer = many to one to costumer models


    """

    id_entidad = models.IntegerField(null=True)
    curp = models.CharField(max_length=18)
    rfc = models.CharField(max_length=15)
    no_credito = models.CharField(max_length=20, blank=True, null=True)
    unidad_credito = models.CharField(max_length=30, blank=True, null=True)
    tipo_moneda = models.CharField(max_length=20, blank=True, null=True)
    T1 = models.FloatField(default=0, null=True)
    T2 = models.FloatField(default=0, null=True)
    T3 = models.DateField(null=True)
    instrumento_monetario = models.IntegerField(null=True)
    canales_distribucion = models.CharField(max_length=30, blank=True,
                                            null=True)
    Estado = models.CharField(max_length=30, blank=True, null=True)
    status_code = models.CharField(max_length=3, blank=True, null=True)
    mensaje = models.CharField(max_length=420, null=True, blank=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='Ucontrato')
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='ContratoCustomer')

    def __str__(self):
        # return str(self.customer)
        return 'MiContrato'
