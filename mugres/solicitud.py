from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class CatalogoCampos(models.Model):
    campo = models.CharField(max_length=40)

    def __str__(self):
        return self.campo

class SolicitudIncompleta(models.Model):
    fechaSolicitud = models.DateTimeField(default=timezone.now)
    catalogo_campos= models.ManyToManyField(
        CatalogoCampos,
        through='Respuestas',
    )
    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='solicitud_incompleta'
    )

class Respuestas(models.Model):
    fechaRespuesta =  models.DateTimeField(null=True)
    catalogoCampos = models.ForeignKey(
        CatalogoCampos,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    solicitudIncompleta = models.ForeignKey(
        SolicitudIncompleta,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
