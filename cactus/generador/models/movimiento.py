# -*- coding: utf-8 -*-


from django.db import models

from spei.models import StpTransaction
from .archivo import Archivo


class Movimiento(models.Model):
    """
    Movimiento asociado a un Archivo de intercambio, para el sistema de
    dispersión de fondos.
    """

    transaccion = models.OneToOneField(StpTransaction,
                                       on_delete=models.CASCADE,
                                       blank=True,
                                       null=True)
    archivo = models.ForeignKey(
        Archivo,
        on_delete=models.CASCADE,
        related_name='movimientos',
        blank=True,
        null=True
    )


class CuentaCargo(models.Model):
    cuenta = models.CharField(
        max_length=11,
        null=True,
        blank=True
    )
    activa = models.BooleanField(default=True)
