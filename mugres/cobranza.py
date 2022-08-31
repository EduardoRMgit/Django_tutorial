from django.db import models
from .transaccion import Transaccion

class Cobranza(models.Model):

    PORCOBRAR = 'PC'
    COBRANDO = 'CE'
    COBRADO = 'C'
    STATUS_COBRANZA_CHOICES = [
        (PORCOBRAR, 'Por Cobrar'),
        (COBRANDO, 'Procezada'),
        (COBRADO, 'Cobrado'),
    ]

    transaccion = models.ForeignKey(
        Transaccion,
        on_delete=models.CASCADE,
        related_name='transaccion_transaccionapago'
    )
    tarjetaDebitoNum = models.CharField(max_length=20,blank=True,null=True)
    monto = models.DecimalField(max_digits=30, decimal_places=4, null=True, blank=True)
    comision = models.DecimalField(max_digits=30, decimal_places=4, null=True,blank=True)
    comisionIVA = models.DecimalField(max_digits=30, decimal_places=4,null=True, blank=True)

    statusCobranza = models.CharField(
        max_length = 2,
        choices = STATUS_COBRANZA_CHOICES,
        default = PORCOBRAR,
    )

    def is_porCobrar(self):
        return self.statusCobranza in (self.PORCOBRAR)

    def is_cobrando(self):
        return self.statusCobranza in (self.COBRANDO)

    def is_Procesada(self):
        return self.statusCobranza in (self.PORCOBRAR, self.COBRANDO)
