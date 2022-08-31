from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class TransactionGpo(models.Model):
    owner = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE
        )

    Fecha = models.DateTimeField(default=timezone.now, null=True, blank=True)
    Servicio = models.CharField(max_length=69)
    Producto = models.CharField(max_length=69)
    Precio = models.CharField(max_length=69)
    Resp = models.CharField(max_length=100, null=True, blank=True,)
    Comision_GPO = models.CharField(max_length=69, blank=True, null=True)
    Comision_BratD = models.DecimalField(null=True, blank=True,
                                         max_digits=14, decimal_places=2)
    Saldo_Cliente = models.DecimalField(null=True, blank=True, max_digits=14,
                                        decimal_places=2, default=0)
    ID_TX = models.CharField(blank=True, null=True, max_length=100)
    Num_Aut = models.CharField(blank=True, null=True, max_length=100)
    codigo = models.CharField(blank=True, null=True, max_length=100)
    Referencia = models.CharField(blank=True, null=True, max_length=100)
    Err = models.CharField(blank=True, null=True, max_length=100)
    stat_code = models.CharField(blank=True, null=True, max_length=100)
    Telefono = models.CharField(blank=True, null=True, max_length=25)

    def __str__(self):
        return str(self.Fecha)

    class Meta():
        verbose_name_plural = 'Transacciones'
