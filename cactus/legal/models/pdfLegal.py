from django.db import models
from django.contrib.auth.models import User


class PdfLegal(models.Model):
    """
    ``Attributes:``
    nombre = CharField(max_length=69, blank=True)
    """
    nombre = models.CharField(max_length=69, blank=True)

    class Meta():
        verbose_name_plural = 'Clausulas Legales'

    def __str__(self):
        return self.nombre


class PdfLegalUser(models.Model):
    """
    ``Attributes:``
    nombre = CharField(max_length=69, blank=True)
    Pdf = FileField(upload_to='docs/pdfLegal', blank=True, null=True)
    fecha = DateTimeField(auto_now=True)
    validado = BooleanField(default=False)
    """

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    nombre = models.ForeignKey(PdfLegal, on_delete=models.DO_NOTHING)
    Pdf = models.FileField(upload_to='docs/pdfLegal', blank=True, null=True)
    fecha = models.DateTimeField(auto_now=True)
    validado = models.BooleanField(default=False)

    class Meta():
        verbose_name_plural = 'Clausulas Legales de Usuario'

    def __str__(self):
        return self.nombre.nombre
