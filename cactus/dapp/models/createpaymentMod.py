from django.db import models
from django.contrib.auth.models import User
from dapp.models import Info
from dapp.models import Payment
from django.core.validators import MaxValueValidator, MinValueValidator


class CreatePay(models.Model):
    class Meta:
        verbose_name_plural = "Crear Pago"

    id_info = models.ForeignKey(
        Info,
        verbose_name="ID Info cobro",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name="Usuario",
        on_delete=models.CASCADE
    )
    cash = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Monto del retiro",
        validators=[
            MaxValueValidator(100000),
            MinValueValidator(0)
        ],
        null=False,
        blank=False
    )
    reference = models.ForeignKey(
        Payment,
        verbose_name="ID Payment",
        on_delete=models.CASCADE
    )

    def __str__(self):
        txt = "ID info: {} / ID user: {}"
        return txt.format(self.id_info, self.user)
