from django.db import models
from .contract import Contrato


class MovimientoD(models.Model):
    """

    ``Attributes:``

    - Descripcion:

    - id_entidad = IntegerField(null=True)
    - id_credito = CharField(max_length=20, blank=True)
    - origen_pago = IntegerField(null=True)
    - tipo_cargo = IntegerField(null=True)
    - tipo_cargo_e = CharField(max_length=45, null=True)
    - tipo_moneda = CharField(max_length=20, null=True)
    - monto_pago = DecimalField(
        max_digits=30, decimal_places=4, null=True, blank=True)
    - fecha_pago = DateField(null=True)
    - comentarios = CharField(max_length=140, null=True)
    - cuenta = IntegerField(null=True)
    - created_at = DateField(null=True)
    - payment_made_by = CharField(max_length=45, null=True)
    - status_code = models.CharField(max_length=3, blank=True, null=True)
    - mensaje = CharField(max_length=420, null=True)
    - contrato = many to one to contrato models
    """
    id_entidad = models.IntegerField(null=True)
    id_credito = models.CharField(max_length=20, blank=True)
    origen_pago = models.IntegerField(null=True)
    tipo_cargo = models.IntegerField(null=True)
    tipo_cargo_e = models.CharField(max_length=45, null=True)
    tipo_moneda = models.CharField(max_length=20, null=True)
    monto_pago = models.DecimalField(
        max_digits=30, decimal_places=4, null=True, blank=True)
    fecha_pago = models.DateField(null=True)
    comentarios = models.CharField(max_length=140, null=True)
    cuenta = models.IntegerField(null=True)
    created_at = models.DateField(null=True)
    payment_made_by = models.CharField(max_length=45, null=True)
    status_code = models.CharField(max_length=3, blank=True, null=True)
    mensaje = models.CharField(max_length=420, null=True)
    contrato = models.ForeignKey(
        Contrato,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='movimiento_contrato')

    def __str__(self):
        return self.id_credito

    class Meta():
        verbose_name_plural = 'UBcubo Movimiento Default'
