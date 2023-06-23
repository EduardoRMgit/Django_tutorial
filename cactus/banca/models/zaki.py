from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from banca.models import Transaccion


class PrestamoZakiTransaccion(models.Model):
    PENDIENTE = 'P'
    LIQUIDADO = 'L'
    VENCIDO = 'V'
    STATUS_PRESTAMO = (
        (PENDIENTE, "Pendiente"),
        (LIQUIDADO, "Liquidado"),
        (VENCIDO, "Vencido"),
    )
    status = models.CharField(
        choices=STATUS_PRESTAMO,
        null=False,
        blank=False,
        default=PENDIENTE,
        max_length=32
    )
    fechaOperacion = models.DateTimeField(default=timezone.now,
                                          null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='prestamos_zaki',
        null=False,
        blank=False
    )
    enviada_prestamo = models.OneToOneField(
        Transaccion,
        related_name="prestamos_enviada",
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    recibida_prestamo = models.OneToOneField(
        Transaccion,
        related_name="prestamos_recibida",
        on_delete=models.CASCADE,
        blank=True,
        null=True)

    monto = models.CharField(max_length=64, null=True)
    monto_total = models.CharField(max_length=64, null=True)

    def __str__(self):
        return f"{self.user.Uprofile.cuentaClabe} - {self.monto_total}"


class PagoZakiTransaccion(models.Model):
    fechaOperacion = models.DateTimeField(default=timezone.now,
                                          null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pagos_zaki',
    )
    enviada_pago = models.OneToOneField(
        Transaccion,
        related_name="pagos_enviada",
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    recibida_pago = models.OneToOneField(
        Transaccion,
        related_name="pagos_recibida",
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    prestamo = models.ForeignKey(
        PrestamoZakiTransaccion,
        on_delete=models.CASCADE,
        related_name='abonos',
        null=True,
        blank=True
    )
    monto = models.CharField(max_length=64, null=True)

    def __str__(self):
        return f"{self.user.Uprofile.cuentaClabe} - {self.monto}"
