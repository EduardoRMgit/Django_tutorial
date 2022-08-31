from django.db import models


# Create your models here.
class Pruebalin(models.Model):
    """
    ``Attributes:``
    nombreArchivo = CharField(max_length=50, blank=True, null=True)

    """

    nombreArchivo = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.depositoRef)
