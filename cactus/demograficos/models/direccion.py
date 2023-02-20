from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils import timezone


class TipoDireccion(models.Model):
    """Address type uploaded by the user.

    ``Attributes:``

        - tipo (char): address type.

    """
    tipo = models.CharField(max_length=30)

    def __str__(self):
        return self.tipo


class EntidadFed(models.Model):
    """State

    ``Attributes:``

        - entidad (char): one of the states of Mexico.

    """
    entidad = models.CharField(max_length=50)
    clave = models.CharField(max_length=2, null=True)

    def __str__(self):
        return self.entidad


class Country(models.Model):

    country = models.CharField(max_length=50)

    def __str__(self):
        return self.country


class Direccion(models.Model):
    """Address

    ``Attributes:``

        - linea1 (char): street, street number, inner number and neighbourhood.

        - linea2 (char): second space for street, street number, inner number \
            and neighbourhood.

        - calle (char 150): Only the street of the adress

        - codPostal (char): zip number.

        - ciudad (char): city.

        - delegMunicipio (char): town.

        - fechaCreacion (datetime): auto added created date and time.

        - activo (bollean): if the address its active or not.

        - validado (boolean): validated with OCR or through an authority \
            process

        - country (countryfield): address' country

        - user (foreign): many to one to the django standard user model.

        - tipo_direccion (foreign): many to one to the TipoDireccion model.

        - entidadFed (foreign): many to one to the entidadFed model.

    """

    linea1 = models.CharField(max_length=150, blank=True, null=True)
    linea2 = models.CharField(max_length=150, blank=True, null=True)
    calle = models.CharField(max_length=150, blank=True, null=True)
    num_int = models.CharField(max_length=30, blank=True, null=True)
    num_ext = models.CharField(max_length=30, blank=True, null=True)
    codPostal = models.CharField(max_length=6, blank=True, null=True)
    colonia = models.CharField(max_length=80, blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    delegMunicipio = models.CharField(max_length=100, blank=True, null=True)
    fechaCreacion = models.DateTimeField(default=timezone.now)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    # Para saber la fecha activa y valida.
    # activo(defaul=true) se modifico a false para que no haya muchos activos
    activo = models.BooleanField(default=False)
    validado = models.BooleanField(default=False, blank=True, null=True)
    country = CountryField(blank=True, null=True)
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
    estado = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Direccion'
        verbose_name_plural = 'Direcciones'

    def __str__(self):
        direccion_completa = '{}{}{}'.format(self.linea1, ', ', self.linea2)
        return direccion_completa
