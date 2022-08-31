from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User


class Institucion(models.Model):
    """Institucion information

    ``Attributes:``

        - nombre (char): Institution's name.

        - limiteCredito (char): ???

        - minPorcentaje (int): ???

        - maxPorcentaje (int): ???

        - user (foreign): many to one to the django standard user model.

        - country (countryfield): user's card country.

    """
    nombre = models.CharField(max_length=80)
    limiteCredito = models.IntegerField(default=2800)
    minPorcentaje = models.IntegerField(default=10)
    maxPorcentaje = models.IntegerField(default=15)
    user = models.ManyToManyField(
        User,
        through='SoyClienteDe',
    )
    country = CountryField()

    class Meta:
        verbose_name = 'Institucion'
        verbose_name_plural = 'Instituciones'

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

    class Meta:
        verbose_name = 'Columna'
        verbose_name_plural = 'Columnas'


class SoyClienteDe(models.Model):
    """Used to make a many to many link.

    ``Attributes:``

        - institucion (foreign): many to one to the Institucion model.

        - user (foreign): many to one to the django standard user model.

    """
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

    class Meta:
        verbose_name_plural = 'Cliente de'


class BinBanco(models.Model):
    """Stores a bank specific bin numer.

    ``Attributes:``

        - bin(char): bank identification number.

        - institucion (foreign): many to one to the Institucion model.

    """
    bin = models.CharField(max_length=6)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)

    def __str__(self):
        return self.bin
