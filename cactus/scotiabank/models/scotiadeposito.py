from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from banca.models import Transaccion, StatusTrans
from django.contrib.auth.models import User


class ScotiaDeposito(models.Model):

    POSSIBLE_STATES = (
        (0, 'Referencia generada'),
        (1, 'Esperando respuesta'),
        (2, 'Depósito recibido'),
        (4, 'Depósito no recibido'),
        (5, 'Error al generar referencia'),
        (6, 'Error en la respuesta'),
    )
    FORMA_PAGO = (
        ('001', 'Efectivo'),
        ('002', 'Cheque nomativo'),
        ('003', 'Transferencia'),
        ('004', 'TDC'),
        ('028', 'TDD'),
    )
    statusTrans = models.IntegerField(choices=POSSIBLE_STATES,
                                      default=0)
    transaccion = models.OneToOneField(Transaccion,
                                       on_delete=models.CASCADE,
                                       blank=True,
                                       null=True)
    fecha_inicial = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True)
    ordenante = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  null=False,
                                  blank=False
                                  )
    referencia_cobranza = models.TextField(max_length=30,
                                           blank=True,
                                           null=True)
    importe_documento = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        null=False,
        blank=False,
        verbose_name="Importe total")
    comision = models.DecimalField(
        default=0,
        null=True,
        blank=True,
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],)
    fecha_limite = models.DateField(
        null=True,
        blank=True,
        auto_now=False,
        auto_now_add=False,
        verbose_name="vigencia de la transacción")
    numero_empresa = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Número de empresa/convenio:',
        default="4572"
    )
    url_comprobante = models.CharField(max_length=2000, null=True, blank=True)
    comprobante_pdf = models.FileField(
        blank=True,
        null=True)
    ubicacion = models.CharField(max_length=64, null=True,
                                 blank=True)
    balance = models.CharField(max_length=10, null=True, blank=True)
    time = models.DateTimeField(default=timezone.now)
    # datos que se meten en la respuesta de scotia
    referencias_resp = models.TextField(max_length=250,
                                        blank=True,
                                        null=True)
    indicador_forma_pago = models.CharField(max_length=3,
                                            choices=FORMA_PAGO,
                                            blank=True,
                                            null=True)
    nombre_plaza_origen = models.CharField(max_length=14,
                                           blank=True,
                                           null=True)
    num_plaza_cobro = models.CharField(max_length=3,
                                       blank=True,
                                       null=True)
    num_sucursal_cobro = models.CharField(max_length=3,
                                          blank=True,
                                          null=True)
    hora_recepcion_pago = models.TimeField(auto_now=False,
                                           auto_now_add=False,
                                           null=True,
                                           blank=False)
    fecha_presentacion_pago = models.DateField(auto_now=False,
                                               auto_now_add=False,
                                               blank=True,
                                               null=True)
    fecha_captura_contable = models.DateField(auto_now=False,
                                              auto_now_add=False,
                                              blank=True,
                                              null=True)
    fecha_aplicacion_recursos = models.DateField(auto_now=False,
                                                 auto_now_add=False,
                                                 blank=True,
                                                 null=True)
    folio_registro = models.CharField(max_length=12, blank=True, null=True)
    numero_folio_total: models.CharField(max_length=7,
                                         blank=True,
                                         null=True)
    archivo_respuesta_H93 = models.ForeignKey(
        "scotiabank.respuestascotia",
        related_name="H83_deposito",
        on_delete=models.SET_NULL,
        blank=True,
        verbose_name="Archivo de respuesta",
        null=True)

    def __str__(self):
        name = str(
            self.ordenante.get_full_name(
            )) + " " + str(self.ordenante.Uprofile.apMaterno)
        return str(name)


@receiver(post_save, sender=ScotiaDeposito)
def actualiza_saldo(sender, instance, created, **kwargs):
    if not created:
        if instance.statusTrans == 2:
            total = float(
                instance.importe_documento)
            status = StatusTrans.objects.get(nombre="exito")
            if instance.transaccion.statusTrans != status:
                padre = Transaccion.objects.get(id=instance.transaccion.id)
                padre.monto = total
                padre.statusTrans = status
                padre.save()
                saldo = float(
                    instance.importe_documento) - float(instance.comision)
                instance.ordenante.Uprofile.saldo_cuenta += saldo
                instance.ordenante.Uprofile.save()
