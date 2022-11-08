from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Payment(models.Model):
    class Meta:
        verbose_name_plural = "Payment"

    id_payment = models.CharField(
        max_length=100,
        verbose_name="ID del pago",
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
    reference_num = models.CharField(
        max_length=100,
        verbose_name="Numero de referencia",
        null=False,
        blank=False
    )
    reference = models.CharField(
        max_length=100,
        verbose_name="Referencia",
        null=False,
        blank=False
    )
    type = models.CharField(
        max_length=100,
        verbose_name="Tipo",
        null=False,
        blank=False
    )
    type_description = models.CharField(
        max_length=100,
        verbose_name="Descripcion de tipo",
        null=False,
        blank=False
    )
    wallet = models.CharField(
        max_length=100,
        verbose_name="Cartera",
        null=False,
        blank=False
    )
    id_wallet = models.CharField(
        max_length=100,
        verbose_name="ID de la cartera",
        null=False,
        blank=False
    )

    def __str__(self):
        txt = "id: {} / monto: ${}"
        return txt.format(self.id_payment, self.amount)
