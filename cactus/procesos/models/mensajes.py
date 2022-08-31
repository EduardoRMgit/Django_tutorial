from django.db import models
from .instituciones import Institucion
from django.utils import timezone


class Mensajes(models.Model):
    INVITACION = 'I'
    NOTIFICACION = 'N'
    EMERGENCIA = 'E'
    PROMOCION = 'P'
    STATUS_CHOICES = (
        (INVITACION, "Invitacion"),
        (NOTIFICACION, "Notificacion"),
        (EMERGENCIA, "Emergencia"),
        (PROMOCION, "Promocion")
    )

    mensaje = models.CharField(max_length=80)
    url = models.CharField(max_length=80)
    fechaEnvio = models.DateTimeField(default=timezone.now)
    fechaResp = models.DateField(null=True)
    fechaCaducidad = models.DateTimeField(default=timezone.now)
    respuestaCliente = models.CharField(max_length=80)
    habilitado = models.BooleanField(default=True)
    explicacion = models.CharField(max_length=80)

    tipo = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=NOTIFICACION
    )

    institucion = models.ForeignKey(
        Institucion,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    # Falta el usuario al que le estamos dando lata
