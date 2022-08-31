# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Catalogo de documentos adjuntos
class DocAdjuntoTipo(models.Model):
    tipo = models.CharField(max_length=30)

    def __str__(self):
        return self.tipo


class DocAdjunto(models.Model):

    #La ruta es dinamica, se construye con la "ruta"
    ruta = models.CharField(max_length=50)
    tipo = models.ForeignKey(
        DocAdjuntoTipo,
        related_name='tipo_documento',
        on_delete=models.CASCADE,
    )
    validado = models.BooleanField(default=False)
    user = models.ForeignKey(
        User,
        related_name='user_documento',
        on_delete=models.CASCADE,
    )
    orden = models.BooleanField(default=True) # 1 es frente 0 es reverso
