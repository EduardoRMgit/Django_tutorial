from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


class Refund(models.Model):
    class Meta:
        verbose_name_plural = "Refund"

    id_refunds = models.CharField(
        max_length=100,
        verbose_name="ID del reembolso",
        null=False,
        blank=False
    )
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Monto del reembolso",
        validators=[
            MaxValueValidator(1000000),
            MinValueValidator(0)
        ],
        null=False,
        blank=False
    )
    currency = models.CharField(
        max_length=10,
        verbose_name="Moneda de cambio",
        null=False,
        blank=False
    )
    date = models.DateField(
        default=timezone.now,
        verbose_name="Fecha de creación"
    )

    def __str__(self):
        txt = 'id: {} / monto: ${} / fecha: {}'
        return txt.format(self.id_refunds, self.amount, self.date)
