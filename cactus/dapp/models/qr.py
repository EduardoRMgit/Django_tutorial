from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Qr(models.Model):

    class Meta:
        verbose_name_plural = "QR"

    qr = models.CharField(
        max_length=50,
        verbose_name="QR ID",
        null=False,
        blank=False
    )
    description = models.CharField(
        max_length=100,
        verbose_name="Descripcion",
        null=True,
        blank=True
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
        max_length=20,
        verbose_name="Mondeda de cambio",
        null=False,
        blank=False
    )
    reference_num = models.CharField(
        max_length=50,
        verbose_name="Número de referencia",
        null=False,
        blank=False
    )

    def __str__(self):
        txt = "qr: {} / monto: ${} "
        return txt.format(self.qr, self.amount, self.amount)
