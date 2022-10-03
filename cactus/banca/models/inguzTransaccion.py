from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from banca.models import Transaccion
from demograficos.models import Contacto


class InguzTransaction(models.Model):

    class Meta:
        verbose_name = "Transaccion Inguz"
        verbose_name_plural = "Transacciones Inguz"

    POSSIBLE_STATES = (
        (0, 'esperando respuesta'),
        (1, 'liquidado'),
        (2, 'devuelto')
    )
    statusTrans = models.IntegerField(choices=POSSIBLE_STATES, default=0)
    rechazada = models.BooleanField(default=False)
    rechazadaMsj = models.CharField(max_length=200, null=True, blank=True)
    fechaOperacion = models.DateTimeField(default=timezone.now,
                                          null=True, blank=True)
    ordenante = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='ordenante',
                                  null=False,
                                  blank=False
                                  )
    transaccion = models.OneToOneField(Transaccion,
                                       on_delete=models.CASCADE,
                                       blank=True,
                                       null=True)
    concepto = models.CharField(max_length=128, null=True, blank=True)
    referencia = models.CharField(max_length=18, null=True)
    causaDevolucion = models.CharField(max_length=64, null=True, blank=True)
    monto = models.CharField(max_length=64, null=True)
    ubicacion = models.CharField(max_length=64, null=True,
                                 blank=True)
    contacto = models.ForeignKey(
        Contacto,
        on_delete=models.CASCADE,
        related_name='contacto_inguz_transaccion',
        blank=True,
        null=True
    )

    def get_main_transaccions(self):
        """
        Returns:
            _type_: Este método regresa todas las transacciones \
            que tengan la misma clave de rastreo que la transacción \
            inguz de salida.
        """
        salida = self.transaccion
        transaccions = Transaccion.objects.filter(
            claveRastreo=salida.claveRastreo)
        return transaccions

    def __str__(self):
        return self.ordenante.Uprofile.cuentaClabe
