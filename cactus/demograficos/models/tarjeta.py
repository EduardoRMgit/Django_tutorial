from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

from .instituciones import Institucion


class StatusTarjeta(models.Model):
    """User's card status.

    ``Attributes:``

        - status (char): user's card status
    """
    status = models.CharField(max_length=60,
                              blank=True,
                              null=True)

    def __str__(self):
        return self.status


class Tarjeta(models.Model):
    """User's card.

    ``Attributes:``

        - tarjetaDebitoNum (char): user's card number.

        - tarjetaDebitoPin (char): user's card pin.

        - country (countryfield): user's card country.

        - user (foreign): many to one to the django standard user model.

        - institucion (foreign): many to one to the Institucion model.

        - statusTarjeta (foreign): many to one to the StatusTarjeta model.
    """
    tarjetaDebitoNum = models.CharField(max_length=20,
                                        blank=True,
                                        null=True)
    tarjetaDebitoPin = models.CharField(max_length=6,
                                        blank=True,
                                        null=True)
    country = CountryField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_tarjeta'
    )
    institucion = models.ForeignKey(
        Institucion,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    statusTarjeta = models.ForeignKey(
        StatusTarjeta,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.tarjetaDebitoNum
