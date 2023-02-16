from django.db import models
from .customer import Customer
from django.utils import timezone


class Movimiento(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='CustomerMovimiento')
    transaccion = models.OneToOneField(
        "banca.transaccion",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='TransaccionPld')
    usuario_pld = models.CharField(max_length=20, null=True)
    curp = models.CharField(max_length=20, null=True)
    origen_pago = models.IntegerField(null=True)
    tipo_cargo = models.IntegerField(null=True)
    tipo_cargo_e = models.CharField(max_length=45, null=True)
    tipo_moneda = models.CharField(max_length=20, null=True)
    monto_pago = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    fecha_pago = models.DateField(null=True)
    comentarios = models.CharField(max_length=45, null=True)
    cuenta = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    payment_made_by = models.CharField(max_length=45, null=True)
    cuentaclabeB = models.CharField(max_length=20, null=True)
    cuentaclabeS = models.CharField(max_length=20, null=True)
    status_code = models.CharField(max_length=3, blank=True, null=True)
    mensaje = models.CharField(max_length=420, null=True, blank=True)

    def __str__(self):
        return self.curp
