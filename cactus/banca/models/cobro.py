from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from banca.models import InguzTransaction


class NotificacionCobro(models.Model):
    PENDIENTE = 'P'
    LIQUIDADO = 'L'
    DECLINADO = 'D'
    VENCIDO = 'V'
    STATUS_COBRO = (
        (PENDIENTE, "Pendiente"),
        (LIQUIDADO, "Liquidado"),
        (DECLINADO, "Declinado"),
        (VENCIDO, "Vencido"),
    )
    usuario_solicitante = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cobros_solicitados'
    )
    usuario_deudor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mis_notificaciones_cobro'
    )
    id_contacto_solicitante = models.IntegerField(
        null=True,
        blank=True
    )
    fecha = models.DateTimeField(
        default=timezone.now
    )
    importe = models.DecimalField(
        max_digits=30,
        decimal_places=4,
        null=True,
        blank=True
    )
    status = models.CharField(
        choices=STATUS_COBRO,
        null=False,
        blank=False,
        default=PENDIENTE,
        max_length=32
    )
    concepto = models.CharField(max_length=512,
                                blank=True,
                                null=True)
    referencia_numerica = models.CharField(max_length=64,
                                           null=True)
    clave_rastreo = models.CharField(max_length=64,
                                     null=True)
    transaccion = models.ForeignKey(
        InguzTransaction,
        on_delete=models.CASCADE,
        related_name='cobros',
        null=True
    )

    class Meta():
        verbose_name_plural = 'Cobros'

    def __str__(self):
        return str(self.importe)
