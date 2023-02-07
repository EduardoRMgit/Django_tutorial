from django.db import models


class Bartola(models.Model):

    class Meta():
        verbose_name = 'Link e imagen'
        verbose_name_plural = 'Links e imágenes'

    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    imagen = models.ImageField(
        upload_to='statics',
        blank=True,
        null=True
    )
    url = models.URLField(
        max_length=300,
        blank=True,
        null=True
    )

    descripcion = models.TextField(
        max_length=300,
        null=True,
        blank=True
    )

    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
