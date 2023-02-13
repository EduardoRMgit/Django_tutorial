from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.core.validators import MinValueValidator
from decimal import Decimal

from .catalogos import (ErroresTransaccion,
                        TipoTransaccion)


class StatusTrans(models.Model):
    nombre = models.CharField(max_length=20)

    class Meta():
        verbose_name_plural = 'Estatus de las Transacciones'

    def __str__(self):
        return self.nombre


class TipoAnual(models.Model):
    nombre = models.CharField(max_length=120)
    numDias = models.IntegerField()

    class Meta():
        verbose_name_plural = 'Tipos Anuales'

    def __str__(self):
        return self.nombre


class Transaccion(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_transaccion'
    )
    """
    receptor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receptor_transaccion'
    )
    """

    """Cuando se solicita el movimiento."""
    fechaValor = models.DateTimeField(
        default=timezone.now)

    """Cuando se ejecuta el movimiento."""
    fechaAplicacion = models.DateTimeField(null=True, blank=True)

    monto = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    statusTrans = models.ForeignKey(
        StatusTrans,
        on_delete=models.SET_NULL,
        related_name='status_transaccion',
        null=True,
        blank=True
    )
    errorRes = models.ForeignKey(
        ErroresTransaccion,
        on_delete=models.SET_NULL,
        related_name='error_transaccion',
        null=True,
        blank=True
    )
    tipoTrans = models.ForeignKey(
        TipoTransaccion,
        on_delete=models.SET_NULL,
        related_name='tipo_transaccion',
        null=True,
        blank=True
    )
    concepto = models.CharField(max_length=250, blank=True, null=True)
    claveRastreo = models.CharField(max_length=64, null=True)

    class Meta():
        verbose_name_plural = 'Transacciones'

    def __str__(self):
        return self.user.username


@receiver(pre_save, sender=Transaccion)
def ejecuta_balanza_notCreated(sender, instance, **kwargs):
    from contabilidad.balanza import balanza
    exito = StatusTrans.objects.get(nombre="exito")
    if instance.id and instance.tipoTrans:
        anterior = Transaccion.objects.get(id=instance.id)
        if (not anterior.statusTrans == instance.statusTrans) and instance.statusTrans == exito:  # noqa: E501
            tipo_trans = int(instance.tipoTrans.codigo)
            if tipo_trans in [1, 2, 3, 6, 18, 19]:
                balanza(instance, tipo_trans)


@receiver(post_save, sender=Transaccion)
def ejecuta_balanza_created(sender, instance, created, **kwargs):
    from contabilidad.balanza import balanza
    exito = StatusTrans.objects.get(nombre="exito")
    if created and instance.statusTrans == exito:
        tipo_trans = int(instance.tipoTrans.codigo)
        if tipo_trans in [1, 2, 3, 6, 18, 19]:
            balanza(instance, tipo_trans)


class TransPago(models.Model):
    transaccion = models.ForeignKey(
        Transaccion,
        on_delete=models.CASCADE,
        related_name='transaccion_transPago'
    )

    pagoTotal = models.DecimalField(max_digits=30, decimal_places=4,
                                    blank=True)
    pagoMonto = models.DecimalField(max_digits=30, decimal_places=4,
                                    blank=True)
    pagoComision = models.DecimalField(max_digits=30, decimal_places=4,
                                       blank=True)
    pagoComisionIVA = models.DecimalField(max_digits=30, decimal_places=4,
                                          blank=True)
    lineaDisponible = models.DecimalField(max_digits=30, decimal_places=4,
                                          blank=True)
    pagadoMonto = models.DecimalField(max_digits=30, decimal_places=4,
                                      blank=True, default=0)
    pagadoComision = models.DecimalField(max_digits=30, decimal_places=4,
                                         blank=True, default=0)
    pagadoComisionIVA = models.DecimalField(max_digits=30, decimal_places=4,
                                            blank=True, default=0)
    fechaPago = models.DateTimeField(default=timezone.now)

    statusTrans = models.ForeignKey(
        StatusTrans,
        on_delete=models.CASCADE,
        related_name='status_transPago'
    )

    class Meta():
        verbose_name_plural = 'Transacciones de Pago'

    def __str__(self):
        return str(self.transaccion.monto)


class TransPagoExterno(models.Model):
    transpago = models.ForeignKey(
        TransPago,
        on_delete=models.CASCADE,
        related_name='transPago_transaccionExterna'
    )
    fechaTrans = models.DateTimeField(default=timezone.now, blank=True)
    errorCode = models.CharField(max_length=10, blank=True)
    noAutorizacion = models.CharField(max_length=120, blank=True)

    class Meta():
        verbose_name_plural = 'Transacciones de Pago Externas'

    def __str__(self):
        return self.noAutorizacion


class ValidacionSesion(models.Model):
    epochExp = models.CharField(max_length=120, blank=True, null=True)
    epoxhOrigIat = models.CharField(max_length=120, blank=True, null=True)
    user = models.CharField(max_length=120, blank=True, null=True)
    fecha = models.DateTimeField(default=timezone.now, blank=True)
    transaccion = models.OneToOneField(
        Transaccion,
        on_delete=models.CASCADE,
        related_name='transaccion_ValidacionSesion',
        null=True,
        blank=True
    )

    class Meta():
        verbose_name_plural = 'Validacion de las sesiones'

    def __str__(self):
        return self.epochExp


class ValidacionTransaccion(models.Model):
    verificacion_db = models.BooleanField(default=False)
    verificacion_https = models.BooleanField(default=False)
    verificacion_intoto = models.BooleanField(default=False)
    transaccion = models.OneToOneField(
        Transaccion,
        on_delete=models.CASCADE,
        related_name='transaccion_ValidacionTransaccion',
        null=True,
        blank=True
    )

    class Meta():
        verbose_name_plural = 'Validacion de las transacciones'

    def __str__(self):
        return str(self.transaccion.user)


class SaldoReservado(models.Model):
    class Meta:
        verbose_name = "Saldo reservado"
        verbose_name_plural = "Saldos reservados"

    STATUS_SALDO = (
        ("reservado", "reservado"),
        ("aplicado", "aplicado"),
        ("devuelto", "devuelto"),
    )
    tipoTrans = models.ForeignKey(
        TipoTransaccion,
        null=True,
        blank=True,
        verbose_name="Tipo de transacción",
        on_delete=models.CASCADE
    )
    status_saldo = models.CharField(
        choices=STATUS_SALDO,
        null=False,
        blank=False,
        default="reservado",
        max_length=20
    )
    fecha_reservado = models.DateTimeField(
        auto_now=False,
        auto_now_add=True
    )
    saldo_reservado = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        null=False,
        blank=False,
        default=0.00
    )
    fecha_aplicado_devuelto = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name="Fecha de aplicación/devolución")

    def __str__(self):
        if self.status_saldo == "reservado":
            a = "SALDO RESERVADO (${})".format(self.saldo_reservado)
        elif self.status_saldo == "aplicado":
            a = "SALDO APLICADO"
        elif self.status_saldo == "devuelto":
            a = "SALDO DEVUELTO (${})".format(self.saldo_reservado)
        txt = "{0}"
        return txt.format(a)
