from django.db import models
from django.utils import timezone
from scotiabank.utility.custom_storage import MediaStorage


class Archivo(models.Model):

    """
        Archivo de intercambio empresa-banco, para el sistema de
        dispersión de fondos.
    """

    STATUS = (
        (0, 'Archivo generado'),
        (1, 'Archivo confirmado por Scotiabank'),
        (2, 'Archivo rechazado por Scotiabank'),
    )
    status = models.IntegerField(
        choices=STATUS,
        default=0,
        verbose_name="Estado",
    )
    errorMsg = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Mensaje de error")
    nombre = models.CharField(max_length=69, blank=True)
    secuencia = models.IntegerField(blank=True, null=True)
    txt = models.FileField(
        storage=MediaStorage(),
        blank=True,
        null=True)
    fecha = models.DateTimeField(default=timezone.now)
    tipo_archivo = models.CharField(
        max_length=50,
        choices=(("Transferencia", "Transferencia"),
                 ("Retiro", "Retiro"),
                 ("Deposito", "Deposito")),
        null=False,
        default=False
    )
    contenido_archivo = models.TextField(null=True, blank=True)
    respuesta_FN5 = models.ForeignKey("scotiabank.respuestascotia",
                                              related_name="FN5_respuesta",
                                              on_delete=models.SET_NULL,
                                              blank=True,
                                              null=True,
                                              verbose_name="Respuesta FN5")

    def __str__(self):
        return self.nombre
