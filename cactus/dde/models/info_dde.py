from django.db import models
from django.contrib.auth.models import User


class DineroDeEmergencia(models.Model):

    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='ddeinfo'
    )

    id_DDE = models.IntegerField(null=True, blank=True)
    fechaCreacion_DDE = models.DateTimeField(null=True, blank=True)
    confirmacion_DDE = models.BooleanField(default=False)
    aceptaKitLegal_DDE = models.DateTimeField(blank=True, null=True)
    saldo_DDE = models.FloatField(null=True, blank=True, default=0)
