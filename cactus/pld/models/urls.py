from django.db import models


# TODOPANDA añadir nombre corto
class UrlsPLD(models.Model):
    """

    ``Attributes:``

    - Descripcion:

    - urls = URLField()

    """
    urls = models.URLField()

    def __str__(self):
        return self.urls

    class Meta:
        verbose_name_plural = 'UBcuboUrlsPLD'
