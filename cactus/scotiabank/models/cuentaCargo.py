from django.db import models


class CuentaCargo(models.Model):
    cuenta = models.CharField(
        max_length=11,
        null=True,
        blank=True
    )
    activa = models.BooleanField(default=True)
