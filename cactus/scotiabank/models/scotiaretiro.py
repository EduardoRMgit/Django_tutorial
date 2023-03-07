from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

from demograficos.models.userProfile import UserProfile
from scotiabank.models import (CatalogoCodigosTEF, ScotiaTransferencia,
                               Archivo)
from banca.models import Transaccion, SaldoReservado, StatusTrans
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver


class ScotiaRetiro(models.Model):
    POSSIBLE_STATES = (
        (0, 'Por procesar'),  # cuando es creado
        (1, 'Archivo generado'),  # cuando se genera archivo
        (2, 'Transacción recibida por Scotiabank'),  # cuando se tenemos FN5
        (4, 'Transacción confirmada por Scotiabank'),  # cuando tenemos FN2
        (5, 'Transacción exitosa (retiro realizado)'),  # cuando tenemos FN3
        (6, 'Error al generar archivo'),  # cuando el archivo se genero mal
        (7, 'Error en el archivo enviado'),  # FN5 con error
        (8, 'Devolución por transacción no procesada'),
        (9, 'Devolución por dinero no retirado'),
    )
    CONCEPTOS_SERVICIO = (
        ('01', 'NOMINA'),
        ('02', 'PENSIONES'),
        ('03', 'OTRAS TRANSFERENCIAS')
    )
    TIPO_CUENTA = (
        (1, 'CUENTA DE CHEQUES'),
        (3, 'CUENTA (TARJETA) DE DEBITO'),
        (9, 'CUENTA DE CHEQUES CLABE')
    )
    fechaOperacion = models.DateTimeField(auto_now=True,
                                          null=True, blank=True)
    fecha_confirmacion = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name='Fecha de confirmación FN3',
    )
    status_codigo = models.ForeignKey(CatalogoCodigosTEF,
                                      on_delete=models.SET_NULL,
                                      blank=True,
                                      null=True)
    statusTrans = models.IntegerField(choices=POSSIBLE_STATES,
                                      default=0)
    rechazoMsg = models.CharField(
        max_length=500,
        verbose_name="Mensaje de rechazo",
        blank=True,
        null=True
    )
    servicio_concepto = models.CharField(max_length=2,
                                         choices=CONCEPTOS_SERVICIO,
                                         default='03')
    transaccion = models.OneToOneField(Transaccion,
                                       on_delete=models.CASCADE,
                                       blank=True,
                                       null=True,
                                       related_name="scotiaRetiro")
    ordenante = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  null=False,
                                  blank=False
                                  )
    tipoCuentaOrdenante = models.IntegerField(choices=TIPO_CUENTA,
                                              default=9)
    monto = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        null=False,
        blank=False)
    comision = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))],
        null=False,
        blank=False
    )
    clave_retiro = models.CharField(max_length=50, null=True, blank=True)
    conceptoPago = models.CharField(
        max_length=50,
        default="Retiro",
        null=True,
        blank=True)
    referenciaPago = models.CharField(max_length=16, null=True, blank=True)
    saldoReservado = models.OneToOneField(
        SaldoReservado,
        null=True,
        blank=True,
        verbose_name="Saldo reservado",
        related_name="scotiaRetiroReservado",
        on_delete=models.CASCADE
    )
    reservado = models.CharField(max_length=64, null=True, default="0")
    archivo = models.ForeignKey(
        Archivo,
        on_delete=models.SET_NULL,
        related_name='retiro',
        blank=True,
        null=True
    )
    numero_empresa = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Número de empresa/convenio:',
        default="17244"
    )
    fecha_limite = models.DateField(
        null=True,
        blank=True,
        auto_now=False,
        auto_now_add=False,
        verbose_name="vigencia de la transacción")
    url_comprobante = models.CharField(max_length=2000, null=True, blank=True)
    comprobante_pdf = models.FileField(
        blank=True,
        null=True)
    archivo_respuesta_FN2 = models.ForeignKey("scotiabank.respuestascotia",
                                              related_name="FN2_retiro",
                                              on_delete=models.SET_NULL,
                                              blank=True,
                                              null=True)
    archivo_resumen = models.ForeignKey("scotiabank.respuestascotia",
                                        related_name="resumen_retiro",
                                        on_delete=models.SET_NULL,
                                        blank=True,
                                        null=True,
                                        verbose_name="Archivo FN3 de resumen")
    ubicacion = models.CharField(max_length=64, null=True,
                                 blank=True)
    balance = models.CharField(max_length=10, null=True, blank=True)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        name = str(
            self.ordenante.get_full_name(
            )) + " " + str(self.ordenante.Uprofile.apMaterno)
        return str(name)


@receiver(pre_delete, sender=Archivo)
def status(sender, instance, **kwargs):

    if instance.tipo_archivo == 'Retiro':
        ScotiaRetiro.objects.filter(
            archivo=instance.id).update(statusTrans=0)
    if instance.tipo_archivo == 'Transferencia':
        ScotiaTransferencia.objects.filter(
            archivo=instance.id).update(statusTrans=0)

    instance.txt.delete()


@receiver(post_save, sender=ScotiaRetiro)
def status_transaction(sender, instance, created, **kwargs):
    if instance.saldoReservado:
        if not created and instance.saldoReservado.status_saldo == "reservado":

            user_profile = UserProfile.objects.get(user=instance.ordenante)
            reservado = SaldoReservado.objects.get(
                id=instance.saldoReservado.id)
            transaction = Transaccion.objects.get(id=instance.transaccion.id)
            statusAplicado = StatusTrans.objects.get(nombre="exito")

            if instance.statusTrans == 5:  # Transacción realizada
                reservado.status_saldo = "aplicado"
                reservado.fecha_aplicado_devuelto = timezone.now()
                reservado.save()
                transaction.monto += reservado.saldo_reservado
                transaction.fechaAplicacion = timezone.now()
                transaction.statusTrans = statusAplicado
                transaction.save()

            if instance.statusTrans == 8 or instance.statusTrans == 9:
                user_profile.saldo_cuenta += float(
                    instance.saldoReservado.saldo_reservado)
                user_profile.save()
                reservado.status_saldo = "devuelto"
                reservado.fecha_aplicado_devuelto = timezone.now()
                reservado.save()
                transaction.fechaAplicacion = timezone.now()
                transaction.statusTrans = statusAplicado
                transaction.save()
