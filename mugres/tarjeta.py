from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils import timezone
from .instituciones import Institucion


class StatusTarjeta(models.Model):
    status = models.CharField(max_length=60,blank=True,null=True)

    def __str__(self):
        return self.status


class Tarjeta(models.Model):
    tarjetaDebitoNum = models.CharField(max_length=20,blank=True,null=True)
    tarjetaDebitoPin = models.CharField(max_length=6,blank=True,null=True)
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

    tatusTarjeta = models.ForeignKey(
        StatusTarjeta,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    def __str__(self):
        return self.tarjetaDebitoNum
