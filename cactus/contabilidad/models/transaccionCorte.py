from django.db import models
from demograficos.models.instituciones import Institucion
from django.utils import timezone


class TransaccionCorteTipo(models.Model):
    """
    ``Attributes:``

    - Descripcion:

    - resumen = many to one to resesumen models
    """
    nombre = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre


class TransaccionCorte(models.Model):
    """
    ``Attributes:``

    - fechaTrans = DateTimeField(default=timezone.now)

    - monto = FloatField()
    - comision = FloatField()
    - comisionIVA = FloatField()
    - institucion = many to one to institucion models
    """

    fechaTrans = models.DateTimeField(default=timezone.now)
    monto = models.FloatField()
    comision = models.FloatField()
    comisionIVA = models.FloatField()
    institucion = models.ForeignKey(
        Institucion,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
