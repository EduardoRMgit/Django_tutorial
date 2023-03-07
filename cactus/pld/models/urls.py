from django.db import models


# TODOPANDA añadir nombre corto
class UrlsPLD(models.Model):
    """

    ``Attributes:``

    - Descripcion:

    - urls = URLField()

    """
    nombre = models.CharField(max_length=50, null=True, blank=True)
    urls = models.URLField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'UBcuboUrlsPLD'
