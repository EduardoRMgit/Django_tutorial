from django.db import models


class adminUtils(models.Model):
    util = models.CharField('Utilidades', max_length=30)
    activo = models.BooleanField(default=False)

    class Meta():
        verbose_name_plural = 'Administrar Utilidades'

    def __str__(self):
        return self.util
