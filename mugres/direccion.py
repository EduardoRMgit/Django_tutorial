from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils import timezone


class TipoDireccion(models.Model):
    tipo = models.CharField(max_length=30)

    def __str__(self):
        return self.tipo


class EntidadFed(models.Model):
    entidad = models.CharField(max_length=50)

    def __str__(self):
        return self.entidad


class Direccion(models.Model):

    linea1 = models.CharField(max_length=50,blank=True)
    linea2 = models.CharField(max_length=50,blank=True)
    codPostal = models.CharField(max_length=6,blank=True)
    ciudad = models.CharField(max_length=50,blank=True)
    delegMunicipio = models.CharField(max_length=50,blank=True)
    fechaCreacion = models.DateTimeField(default=timezone.now)
    # Para saber la fecha activa y valida.
    activo = models.BooleanField(default=False)
    validado = models.BooleanField(default=False)
    country = CountryField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_direccion'
    )
    tipo_direccion = models.ForeignKey(
        TipoDireccion,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    entidadFed = models.ForeignKey(
        EntidadFed,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        direccion_completa = '{}{}{}'.format(self.linea1,', ',self.linea2) 
        return direccion_completa
