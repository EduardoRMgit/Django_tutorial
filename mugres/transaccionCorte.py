from django.db import models
from .instituciones import Institucion
from django.utils import timezone


class TransaccionCorteTipo(models.Model):
    nombre = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre


class TransaccionCorte(models.Model):

    fechaTrans = models.DateTimeField(default=timezone.now)
    monto  = models.FloatField()
    comision  = models.FloatField()
    comisionIVA  = models.FloatField()
    institucion = models.ForeignKey(
        Institucion,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
