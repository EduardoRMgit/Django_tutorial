from django.db import models
from .instituciones import Institucion
from django.contrib.auth.models import User


class Prospectos(models.Model):
    referencia = models.CharField(max_length=80)
    tarjeta = models.CharField(max_length=16)
    telefono = models.CharField(max_length=20, null=True)
    vecesDeContacto = models.IntegerField(default=0)
    candidato = models.BooleanField(default=False)
    sumaTotal = models.FloatField(default=0)
    promedio = models.FloatField(default=0)
    limiteCreditoReal = models.FloatField(default=0)
    limiteCreditoRedondeado = models.FloatField(default=0)
    maximo = models.FloatField(default=0)
    minimo = models.FloatField(default=0)
    desvEst = models.FloatField(default=0,null=True, blank=True)
    porcentaje = models.FloatField(default=10)
    depositosPromedio = models.FloatField(default=0)
    fechaCreacion = models.DateTimeField(auto_now=True)
    formato = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='Uprospecto')

    def __str__(self):
        return self.referencia


class Depositos(models.Model):
    identificador = models.IntegerField(default=1)
    fecha = models.DateField()
    importe = models.FloatField()
    prospecto = models.ForeignKey(Prospectos, on_delete=models.CASCADE)

class DepositosRaw(models.Model):
    identificador = models.IntegerField()
    fecha = models.DateField()
    importe = models.FloatField()
    Tarjeta = models.IntegerField()
    #prospecto = models.ForeignKey(Prospectos, on_delete=models.CASCADE)

class ProspectosRaw(models.Model):
    depositosID = models.IntegerField()
