from django.db import models
from django.contrib.auth.models import User
from banca.models.catalogos import CAMI
from django.utils import timezone


class ComportamientoDiario(models.Model):
    """
    ``Attributes:``
        - excesotransaccion (boolean): Limite de transaccion default=False
        - fecha (datetime): fecha creada
        - monto (decimal): cantidad en decimales y con limite null=True,
          blank=True, default=0,decimal_places=2,max_digits=10
        - numtrans (float)= numero de transaccionecimal null=True, blank=True,
          default=0
        - user (foregin): many to one to user model
    """
    excesotransaccion = models.BooleanField(default=False)
    fecha = models.DateField(default=timezone.now)
    monto = models.DecimalField(null=True, blank=True, default=0,
                                decimal_places=2, max_digits=10)
    numtrans = models.FloatField(null=True, blank=True, default=0)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_comportamientod'
    )


class ComportamientoMensual(models.Model):
    """
    ``Attributes:``
        - user (foreignein):many to one to user
        - fecha (datatime): fecha creada
        - retiroMensualTotal (decimal):retiro mesual client null=True,
          blank=True, default=0, decimal_places=2, max_digits=10
        - depositoMensualTotal (decimal): cantidad mensual en decimales
          decimal_places=2, max_digits=10,default=0
          null=True, blank=True,
        - montoInusualMensual (foregin):many to one to CAMID models
          blank=True,
        - numretiros (integer):cantidad de retiros null=True, blank=True,
          default=0
        - numdepositos (integer):cantidad de depositos null=True, blank=True,
          default=0
        - depositoMensualPromedio (decimal):promedio mensual null=True,
          blank=True,default=0,decimal_places=2,max_digits=10
        - retiroMensualPromedio (decimal):cantidad retirada mensualmente
          null=True, blank=True,default=0,decimal_places=2,max_digits=10
        - alarmaretiro (bool):cantidad limite de retiro default=False
        - alarmadeposito (bool):cantidad maxima deposito default=False
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_comportamientom'
    )
    fecha = models.DateField(default=timezone.now)
    retiroMensualTotal = models.DecimalField(null=True, blank=True, default=0,
                                             decimal_places=2, max_digits=10)
    depositoMensualTotal = models.DecimalField(null=True, blank=True,
                                               default=0,
                                               decimal_places=2, max_digits=10)
    montoInusualMensual = models.ForeignKey(
        CAMI,
        on_delete=models.SET_NULL,
        related_name='CAMIM_comportamiento',
        null=True,
        blank=True
    )
    numretiros = models.IntegerField(null=True, blank=True, default=0)
    numdepositos = models.IntegerField(null=True, blank=True, default=0)
    depositoMensualPromedio = models.DecimalField(null=True, blank=True,
                                                  default=0,
                                                  decimal_places=2,
                                                  max_digits=10)
    retiroMensualPromedio = models.DecimalField(null=True, blank=True,
                                                default=0,
                                                decimal_places=2,
                                                max_digits=10)
    alarmaretiro = models.BooleanField(default=False)
    alarmadeposito = models.BooleanField(default=False)
