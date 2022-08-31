from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils import timezone


class TipoTelefono(models.Model):
    tipo = models.CharField(max_length=30)

    def __str__(self):
        return self.tipo

class ProveedorTelefonico(models.Model):
    proveedor = models.CharField(max_length=30)
    country = CountryField()

    def __str__(self):
        return self.proveedor

class Telefono(models.Model):

    telefono = models.CharField(max_length=12)
    extension = models.CharField(max_length=6,blank=True)
    fechaCreacion = models.DateTimeField(default=timezone.now)
    country = CountryField()
    codigos = models.CharField(max_length=20,blank=True)
    activo = models.BooleanField(default=False)
    validado = models.BooleanField(default=False)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_telefono'
    )

    proveedorTelefonico = models.ForeignKey(
        ProveedorTelefonico,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    tipoTelefono = models.ForeignKey(
        TipoTelefono,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.telefono)
