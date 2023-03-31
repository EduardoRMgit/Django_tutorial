from django.db import models
from django.utils import timezone


class AlertasPLD(models.Model):
    descripcion = models.CharField(max_length=1056)
    fecha = models.DateTimeField(default=timezone.now)
    motivo = models.CharField(max_length=1056)

    def __str__(self):
        return self.motivo
