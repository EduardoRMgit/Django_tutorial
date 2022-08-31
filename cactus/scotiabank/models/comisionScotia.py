from django.core.validators import MinValueValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from decimal import Decimal
from django.db import models


class ComisionesScotia (models.Model):

    class Meta:
        verbose_name = "Comisión de scotiabank"
        verbose_name_plural = "Comisiones de scotiabank"

    transaccion = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        verbose_name="Transacción")

    comision_scotia = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        null=False,
        blank=False,
        verbose_name="Comisión Scotiabank sin IVA")

    iva = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        null=True,
        blank=True,
        verbose_name="IVA")

    comision_inguz = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        null=False,
        blank=False,
        default=0,
        verbose_name="Comisión Inguz")
    comision_total = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        null=True,
        blank=True,
        verbose_name="Comisión a cobrar")

    def __str__(self):
        txt = "{0}"
        return txt.format(self.transaccion)


@receiver(pre_save, sender=ComisionesScotia)
def calcula_iva(sender, instance, **kwargs):
    iva = float(instance.comision_scotia) * 0.16
    total = iva + float(instance.comision_scotia + instance.comision_inguz)
    instance.comision_total = total
    instance.iva = iva
