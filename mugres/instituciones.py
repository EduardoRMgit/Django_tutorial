from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User


class Institucion(models.Model):
    nombre = models.CharField(max_length=80)
    limiteCredito = models.IntegerField(default=2800)
    minPorcentaje = models.IntegerField(default=10)
    maxPorcentaje = models.IntegerField(default=15)
    user = models.ManyToManyField(
        User,
        through='SoyClienteDe',
    )
    country = CountryField()

    def __str__(self):
        return self.nombre


class Columnas(models.Model):
    nombre = models.CharField(max_length=80)
    equivalencia = models.CharField(max_length=80)
    nombreSalida = models.CharField(max_length=80)
    default = models.CharField(max_length=80)
    formato = models.CharField(max_length=80)
    comentario = models.CharField(max_length=80)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)


class SoyClienteDe(models.Model):
    institucion = models.ForeignKey(
        Institucion,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )


class BinBanco(models.Model):
    bin = models.CharField(max_length=6)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)

    def __str__(self):
        return self.bin
