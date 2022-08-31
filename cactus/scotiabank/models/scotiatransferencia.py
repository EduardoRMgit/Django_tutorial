from django.db import models
from spei.models import InstitutionBanjico
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.db.models.signals import pre_save
from django.dispatch import receiver
from scotiabank.models import (CatalogoCodigosTEF,
                               Archivo)
from banca.models import Transaccion
from django.utils import timezone
from django.contrib.auth.models import User


class ScotiaTransferencia(models.Model):
    POSSIBLE_STATES = (
        (0, 'Por procesar'),  # cuando es creado
        (1, 'Archivo generado'),  # cuando se genera archivo
        (2, 'Transacción enviada'),  # cuando se envia archivo
        (4, 'Transacción recibida con éxito'),  # cuando tenemos FN2
        (5, 'Transacción realizada'),  # cuando tenemos FN5
        (6, 'Error al generar archivo'),  # ccuando el archivo se genero mal
        (7, 'Error al enviar archivo'),  # cuando tiene error interno
        (8, 'Transacción fallida'),  # la respuesta fue rechazada
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
    TIPO_TRANSFERENCIA = (
        ('interbancaria', 'Interbancaria'),
        ('interna', 'Interna')
    )

    tipo_trans = models.CharField(max_length=20,
                                  choices=TIPO_TRANSFERENCIA,
                                  null=True,
                                  blank=True,
                                  verbose_name="Tipo de transferencia"
                                  )
    status_codigo = models.ForeignKey(CatalogoCodigosTEF,
                                      on_delete=models.SET_NULL,
                                      blank=True,
                                      null=True)
    statusTrans = models.IntegerField(choices=POSSIBLE_STATES,
                                      default=0)
    servicio_concepto = models.CharField(max_length=2,
                                         choices=CONCEPTOS_SERVICIO,
                                         default='03')
    institucionBeneficiariaInt = models.ForeignKey(InstitutionBanjico,
                                                   on_delete=models.DO_NOTHING,
                                                   blank=False,
                                                   null=False,
                                                   related_name='iB_iB_2')
    transaccion = models.OneToOneField(Transaccion,
                                       on_delete=models.CASCADE,
                                       blank=True,
                                       null=True)
    monto = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        null=False,
        blank=False)
    comision = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        null=False,
        blank=False)
    fechaOperacion = models.DateTimeField(default=timezone.now,
                                          null=True, blank=True)
    ordenante = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  null=False,
                                  blank=False
                                  )
    nombreBeneficiario = models.CharField(max_length=40,
                                          null=False,
                                          blank=False)
    tipoCuentaBeneficiario = models.IntegerField(choices=TIPO_CUENTA,
                                                 default=9)
    cuentaBeneficiario = models.CharField(max_length=20, null=True,
                                          blank=True)
    rfcCurpBeneficiario = models.CharField(max_length=18, null=True,
                                           blank=True)
    clave_beneficiario = models.CharField(max_length=20, null=False,
                                          blank=False)
    conceptoPago = models.CharField(max_length=50, null=True, blank=True)
    referenciaPago = models.CharField(max_length=16, null=True, blank=True)
    archivo = models.ForeignKey(
        Archivo,
        on_delete=models.SET_NULL,
        related_name='archivo',
        blank=True,
        null=True
    )
    archivo_respuesta_FN2 = models.ForeignKey("scotiabank.respuestascotia",
                                              related_name="FN2_transaccion",
                                              on_delete=models.SET_NULL,
                                              blank=True,
                                              null=True)
    archivo_respuesta_FN5 = models.ForeignKey("scotiabank.respuestascotia",
                                              related_name="FN5_transaccion",
                                              on_delete=models.SET_NULL,
                                              blank=True,
                                              null=True)
    archivo_resumen = models.ForeignKey("scotiabank.respuestascotia",
                                        related_name="resumen_transaccion",
                                        on_delete=models.SET_NULL,
                                        blank=True,
                                        null=True)
    ubicacion = models.CharField(max_length=64, null=True,
                                 blank=True)
    balance = models.CharField(max_length=10, null=True, blank=True)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        txt = '{0} > {1}'
        return txt.format(
            self.ordenante.get_full_name(),
            self.nombreBeneficiario)


@receiver(pre_save, sender=ScotiaTransferencia)
def define_comision(sender, instance, **kwargs):
    if instance.id is None:
        if instance.institucionBeneficiariaInt.id == 13:
            instance.comision = 4.00   # luego con el eval desde comisiones
            instance.tipo_trans = "interna"
        else:
            instance.comision = 7.00   # luego con el eval desde comisiones
            instance.tipo_trans = "interbancaria"
