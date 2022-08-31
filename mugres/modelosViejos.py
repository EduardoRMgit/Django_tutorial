from django.db import models
from django.utils import timezone


class NominaPrecarga(models.Model):

    empleadoraID = models.CharField(max_length=20)
    numNomina = models.CharField(max_length=80)
    antiguedad = models.CharField(max_length=80)
    sueldoQuincenal = models.CharField(max_length=30)
    lineaCreditoSugerida = models.FloatField()
    telCelular = models.CharField(max_length=15)
    referencia = models.CharField(max_length=80)


class LogWebIngreso(models.Model):

    ipOrigen = models.CharField(max_length=20)
    metodo = models.CharField(max_length=80)
    fecha = models.DateTimeField(default=timezone.now)
    modulo = models.CharField(max_length=30)
    adicional = models.CharField(max_length=30)
    telCelular = models.CharField(max_length=15)
    nombre = models.CharField(max_length=80)
    tarjetaDebitoNum = models.CharField(max_length=16)
