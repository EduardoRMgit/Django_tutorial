from django.db import models
from .productos import Productos


# Lista de Medios disponibles que tiene el producto.
class MediosDisponibles(models.Model):

    medio = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)

    productos = models.ManyToManyField(Productos)

    def __str__(self):
        return self.medio
