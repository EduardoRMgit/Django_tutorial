from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class CatalogoCampos(models.Model):
    """Used for clasifying applications.

    ``Attributes:``

        - campo (char): user's card number.
    """
    campo = models.CharField(max_length=40)

    def __str__(self):
        return self.campo


class SolicitudIncompleta(models.Model):
    """User's card.

    ``Attributes:``

        - fechaSolicitud (dateTime): date created.

        - catalogo_campos (ManyToMany): link with CatalogoCampos model
            through Respuestas

        - user (foreign): many to one to the django standard user model.
    """
    fechaSolicitud = models.DateTimeField(default=timezone.now)
    catalogo_campos = models.ManyToManyField(
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
    """New answer to a single application.

    ``Attributes:``

        - fechaRespuesta (dateTime): date created.

        - catalogo_campos (foreign): link with CatalogoCampos model.

        - solicitudIncompleta (foreign): link with SolicitudIncompleta model.
    """
    fechaRespuesta = models.DateTimeField(null=True)
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
