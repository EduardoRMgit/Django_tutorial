from django.db import models
from .instituciones import Institucion
from django.contrib.auth.models import User
from .transaccion import Transaccion
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class TransPago_AuthHead(models.Model):

    nombreArchivo = models.CharField(max_length=50, blank=True, null=True)
    depositoRef = models.CharField(max_length=50, blank=True, null=True)
    fechaArchivo = models.DateTimeField(null=True)
    fechaOperacion = models.DateTimeField(null=True)
    fechaAutorizado = models.DateTimeField(null=True)
    montoTotalPagos = models.DecimalField(max_digits=30, decimal_places=4,
                                          blank=True)
    numRegistros = models.DecimalField(max_digits=30, decimal_places=4,
                                       blank=True)

    institucion = models.ForeignKey(
        Institucion,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='TransPago_AuthHead',
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.depositoRef)


class TransPago_AuthDet(models.Model):

    monto = models.DecimalField(max_digits=30, decimal_places=4, blank=True)
    fechaAplicacion = models.DateTimeField(null=True)
    noAuth = models.CharField(max_length=50, blank=True, null=True)
    statusPago = models.CharField(max_length=10, blank=True, null=True)
    statusCliente = models.CharField(max_length=10, blank=True, null=True)

    transaccion = models.ForeignKey(
        Transaccion,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    transPago_AuthHead  = models.ForeignKey(
        TransPago_AuthHead,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.noAuth)


class UploadBNXOutSetSVA(models.Model):
    upload = models.FileField(storage=FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, 'BNMX_OUTSETSVA')))
    fechaUpload = models.DateTimeField(null=True)


class UploadTefOut(models.Model):
    upload = models.FileField(storage=FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, 'BNMX_OUTSETSVA')))
    fechaUpload = models.DateTimeField(null=True)
