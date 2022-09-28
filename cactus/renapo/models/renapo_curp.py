from django.db import models
from django.contrib.auth.models import User


class Renapo(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='Usuario_Renapo',
        unique=True)

    curp = models.CharField(max_length=18, null=True, blank=True)
    renapo_resp = models.CharField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Respuesta de RENAPO",
    )
    renapo_nombre = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Nombre en Renapo",
    )
    renapo_ap_pat = models.CharField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Apellido paterno en RENAPO",
    )
    renapo_ap_mat = models.CharField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Apellido materno en RENAPO",
    )
    renapo_nacimiento = models.CharField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Fecha de nacimiento en RENAPO",
    )

    msjError = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Mensaje de validación")

    exitoso = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
