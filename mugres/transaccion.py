from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .productos import Productos, CarProducto


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

    VIGENTE = 'V'
    COBRANDO = 'CE'
    COBRADO = 'C'

    STATUS_COBRANZA_CHOICES = [
        (VIGENTE, 'Vigente'),
        (COBRANDO, 'Enviado a Cobro'),
        (COBRADO, 'Cobrado'),
    ]

    VENCIDA = 'VE'
    INCOBRABLE = 'IN'
    STATUS_VENCIMIENTO_CHOICES = [
        (VIGENTE, 'Vigente'),
        (VENCIDA, 'Vencida'),
        (INCOBRABLE, 'Incobrable'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_transaccion'
    )

    fechaTrans = models.DateTimeField(default=timezone.now, null=True, blank=True)
    fechaVencimiento = models.DateTimeField()
    monto = models.DecimalField(max_digits=30, decimal_places=4, null=True, blank=True)
    comision = models.DecimalField(max_digits=30, decimal_places=4, null=True,blank=True)
    comisionIVA = models.DecimalField(max_digits=30, decimal_places=4,null=True, blank=True)
    pagadoMonto = models.DecimalField(max_digits=30, decimal_places=4, null=True,blank=True,default=0)
    pagadoComision = models.DecimalField(max_digits=30, decimal_places=4, null=True,blank=True,default=0)
    pagadoComisionIVA = models.DecimalField(max_digits=30, decimal_places=4, null=True,blank=True,default=0)
    porcentajeComision = models.DecimalField(max_digits=30, decimal_places=4, null=True,blank=True,default=12)
    porcentajeComisionIVA = models.DecimalField(max_digits=30, decimal_places=4, null=True,blank=True,default=16)
    fechaLiquidacion = models.DateTimeField(null=True, blank=True)

    productos = models.ForeignKey(
        Productos,
        on_delete=models.CASCADE,
        related_name='producto_transaccion'

    )

    statusTrans = models.ForeignKey(
        StatusTrans,
        on_delete=models.CASCADE,
        related_name='status_transaccion'
    )

    tipoAnual = models.ForeignKey(
        TipoAnual,
        on_delete=models.CASCADE,
        related_name='tipoAnual_transaccion'
    )

    statusCobranza = models.CharField(
        max_length = 2,
        choices = STATUS_COBRANZA_CHOICES,
        default = VIGENTE,
        null = True,
        blank = True,
    )

    statusVencimiento = models.CharField(
        max_length = 2,
        choices = STATUS_VENCIMIENTO_CHOICES,
        default = VIGENTE,
        null = True,
        blank = True,
    )

    class Meta():
        verbose_name_plural = 'Transacciones'


    def __str__(self):
        return self.user.username

class TransaccionExterna(models.Model):

    transaccion = models.ForeignKey(
        Transaccion,
        on_delete=models.CASCADE,
        related_name='transaccion_transaccionExterna'
    )
    fechaTrans = models.DateTimeField(default=timezone.now)
    errorCode = models.IntegerField(blank=True, null=True)
    noAutorizacion = models.CharField(max_length=120)
    quien = models.CharField(max_length=120, blank=True)

    class Meta():
        verbose_name_plural = 'Transacciones Externas'

    def __str__(self):
        return self.noAutorizacion


class TransPago(models.Model):
    transaccion = models.ForeignKey(
        Transaccion,
        on_delete=models.CASCADE,
        related_name='transaccion_transPago'
    )

    pagoTotal = models.DecimalField(max_digits=30, decimal_places=4,blank=True)
    pagoMonto = models.DecimalField(max_digits=30, decimal_places=4, blank=True)
    pagoComision = models.DecimalField(max_digits=30, decimal_places=4, blank=True)
    pagoComisionIVA = models.DecimalField(max_digits=30, decimal_places=4, blank=True)
    lineaDisponible = models.DecimalField(max_digits=30, decimal_places=4, blank=True)
    pagadoMonto = models.DecimalField(max_digits=30, decimal_places=4, blank=True,default=0)
    pagadoComision = models.DecimalField(max_digits=30, decimal_places=4, blank=True,default=0)
    pagadoComisionIVA = models.DecimalField(max_digits=30, decimal_places=4, blank=True,default=0)
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

class LogExportadoTrans(models.Model):
    transaccion = models.ForeignKey(
        Transaccion,
        on_delete=models.CASCADE,
        related_name='transaccion_logExportadoTrans'
    )
    fechaExportacion = models.DateTimeField(blank=True, null=True)
    referencia = models.CharField(max_length=120, blank=True, null=True)
    fechaConfirmado = models.DateTimeField(blank=True, null=True)
    fechaCobranza = models.DateTimeField(blank=True, null=True)
    fechaConfirmadoCobranza = models.DateTimeField(blank=True, null=True)

    class Meta():
        verbose_name_plural = 'Logs de Transacciones'

    def __str__(self):
        return self.referencia


class TransaccionCancelada(models.Model):

    fechaTrans = models.DateTimeField(default=timezone.now, blank=True)
    errorCode = models.CharField(max_length=10, blank=True)
    noAutorizacion = models.CharField(max_length=50, blank=True)
    errorDesc = models.CharField(max_length=100, blank=True)

    class Meta():
        verbose_name_plural = 'Transacciones Canceladas'

    def __str__(self):
        return self.noAutorizacion
