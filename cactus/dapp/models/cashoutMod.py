from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class CashoutM(models.Model):
    class Meta:
        verbose_name_plural = "Cashout"

    id_cashout = models.CharField(
        max_length=100,
        verbose_name="ID del retiro",
        null=False,
        blank=False
    )
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Monto",
        validators=[
            MaxValueValidator(100000),
            MinValueValidator(0)
        ],
        null=False,
        blank=False
    )
    currency = models.CharField(
        max_length=50,
        verbose_name="Moneda de cambio",
        null=False,
        blank=False
    )

    def __str__(self):
        txt = "id: {} / monto: ${}"
        return txt.format(self.id_cashout, self.amount)
