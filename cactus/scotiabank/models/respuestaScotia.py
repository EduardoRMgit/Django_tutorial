from scotiabank.utility.ScotiaResp import ParserScotia
from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from urllib.parse import urlparse
import logging


class RespuestaScotia(models.Model):

    class Meta:
        verbose_name = "Respuesta de scotiabank"
        verbose_name_plural = "Respuestas scotiabank"

    TIPO = (
        ('000', 'Por definir'),
        ('FN2', 'Confirmación de movimiento generado'),
        ('FN3', 'Resumen movimientos día anterior'),
        ('FN4', 'Resumen de rechazo día anterior'),
        ('FN5', 'Respuesta de recibido'),
        ('H83', 'Resumen de cobranza con recibo (DEF 1'),
        ('H93', 'Resumen de cobranza con recibo (DEF 2)'),
        ('###', 'Inválido (no definido)')
    )
    fecha = models.DateTimeField(auto_now=True)
    tipo = models.CharField(
        choices=TIPO,
        max_length=3,
        null=True,
        blank=True,
        default='000'
    )
    nombre_archivo = models.CharField(
        max_length=56,
        blank=True,
        null=True,
        verbose_name="Nombre del archivo",
        validators=[MinLengthValidator(52)]
    )
    contenido = models.TextField(
        null=True,
        blank=True
    )
    url_respuesta = models.URLField(max_length=2056, blank=True, null=True)

    def __str__(self):
        txt = "{0}"
        return txt.format(self.nombre_archivo)


@receiver(post_save, sender=RespuestaScotia)
def archivo(sender, instance, created, **kwargs):
    if created:
        db_logger = logging.getLogger("db")
        url = instance.url_respuesta
        if url:
            nombre = (urlparse(url)).path
            nombre = nombre.split("/")[-1]

            response = requests.get(url)
            instance.nombre_archivo = nombre
            contenido = response.__dict__["_content"].decode('latin1')
            instance.contenido = contenido
            if contenido is None or contenido == "":
                db_logger.error(
                    "[ScotiaBank Error] El archivo de respuesta '{}'. \
                        del servicio H2H se recibió vacío. No se procesará \
                        ningun movimiento de esa respuesta.\
                        ".format(
                        nombre
                    )
                )
                valido = False
            else:
                valido = True

            if "FN2" in nombre and not (".pdf" in nombre):
                instance.tipo = "FN2"
                instance.save()
                if valido is True:
                    ParserScotia.FN2(nombre, contenido, instance)

            elif "FN3" in nombre and not (".pdf" in nombre):
                instance.tipo = "FN3"
                instance.save()
                if valido is True:
                    ParserScotia.FN3(nombre, contenido, instance)

            elif "FN4" in nombre and not (".pdf" in nombre):
                instance.tipo = "FN4"
                instance.save()

            elif "FN5" in nombre and not (".pdf" in nombre):
                instance.tipo = "FN5"
                instance.save()
                if valido is True:
                    ParserScotia.FN5(nombre, contenido, instance)

            elif "H93" in nombre and not (".pdf" in nombre):
                instance.tipo = "H93"
                instance.save()
                if valido is True:
                    ParserScotia.H93(nombre, contenido, instance)
            elif "H83" in nombre and not (".pdf" in nombre):
                instance.tipo = "H83"
                instance.save()

            else:
                instance.tipo = "###"
                instance.save()
