# -*- coding: utf-8 -*-


from django.db import models


class Archivo(models.Model):
    """
    Archivo de intercambio empresa-banco, para el sistema de
    dispersión de fondos.
    """

    nombre = models.CharField(max_length=69, blank=True)
    secuencia = models.IntegerField(blank=True, null=True)
    txt = models.FileField(upload_to='docs/archivo', blank=True, null=True)
    fecha = models.DateTimeField(auto_now=True)

    class Meta():
        verbose_name_plural = 'Archivo de intercambio'

    def __str__(self):
        return self.nombre
