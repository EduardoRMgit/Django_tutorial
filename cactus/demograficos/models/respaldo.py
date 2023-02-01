from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Respaldo(models.Model):

    class Meta():
        verbose_name_plural = 'Respaldos'

    STATUS = (
        ("A", "APROBADA"),
        ("P", "PENDIENTE"),
        ("D", "DECLINADA"),
        ("V", "VENCIDA")
    )

    status = models.CharField(
        default="P",
        verbose_name="Solicitud",
        max_length=10,
        choices=STATUS,
    )

    ordenante = models.ForeignKey(
        User,
        verbose_name="Usuario",
        related_name="respaldos",
        on_delete=models.CASCADE
    )

    respaldo = models.ForeignKey(
        User,
        related_name="respaldados",
        on_delete=models.CASCADE
    )

    fecha_solicitud = models.DateTimeField(default=timezone.now)

    contacto_id = models.PositiveSmallIntegerField(
        verbose_name="ID del contacto",
        null=True,
        blank=True
    )

    contrato = models.FileField(
        null=True,
        blank=True,
        upload_to="contratos-respaldos",
        max_length=100
    )

    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.respaldo.username
