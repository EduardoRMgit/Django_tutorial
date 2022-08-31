from django.db import models
from .catalogos import CAMI
from .transaccion import Transaccion


class ValidacionRegulatoria(models.Model):
    alarma = models.BooleanField(default=False)
    idCAMID = models.ForeignKey(
       CAMI,
       on_delete=models.CASCADE,
       related_name='validacionR_CAMID'
    )
    transaccion = models.OneToOneField(
        Transaccion,
        on_delete=models.CASCADE,
        related_name='transaccion_validacioR',
        null=True,
        blank=True
    )
