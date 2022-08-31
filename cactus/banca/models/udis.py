from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save


class ValorUdis(models.Model):

    balance = models.DecimalField(decimal_places=4, max_digits=16,
                                          null=True, blank=True)
    valor_monetario = models.DecimalField(decimal_places=6, max_digits=15,
                                          null=True, blank=True)
    udis_cuenta = models.DecimalField(decimal_places=4, max_digits=15,
                                          null=True, blank=True)

    def __str__(self):
        return str(self.valor_monetario)

    class Meta:
        verbose_name_plural = 'Valor Udis'


@receiver(pre_save, sender=ValorUdis)
def udis(sender, instance, **kwargs):
    instance.udis_cuenta = instance.balance / instance.valor_monetario
