from django.db import models
from dapp.models import CreatePay
from dapp.models import Merchant
from django.contrib.auth.models import User
from dapp.models import Qr
from django.core.validators import MaxValueValidator, MinValueValidator
from dapp.models import Payment
from dapp.models import Refund
from dapp.models import Category
from dapp.models import Terminal
from dapp.models import CashoutM
from django.utils import timezone


class RealizarP(models.Model):
    class Meta:
        verbose_name_plural = "Realizar pago"

    id_ticket = models.CharField(
        max_length=50,
        verbose_name="ID del ticket",
        null=False,
        blank=False
    )
    id_create = models.ForeignKey(
        CreatePay,
        verbose_name="ID de la creacion del pago",
        on_delete=models.CASCADE
    )
    id_merch = models.ForeignKey(
        Merchant,
        verbose_name="ID del comercio",
        on_delete=models.CASCADE
    )
    currency = models.CharField(
        max_length=50,
        verbose_name="Moneda de cambio",
        null=False,
        blank=False
    )
    user = models.ForeignKey(
        User,
        verbose_name="Usuario",
        on_delete=models.CASCADE
    )
    reference = models.CharField(
        max_length=50,
        verbose_name="Numero de referencia",
        null=False,
        blank=False
    )
    id_qr = models.ForeignKey(
        Qr,
        verbose_name="ID de QR",
        on_delete=models.CASCADE
    )
    date = models.DateField(
        default=timezone.now,
        verbose_name="Fecha de pago"
    )
    refunded = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Reembolso",
        validators=[
            MaxValueValidator(100000),
            MinValueValidator(0)
        ],
        null=False,
        blank=False
    )
    id_pay = models.ForeignKey(
        Payment,
        verbose_name="ID del pago",
        on_delete=models.CASCADE
    )
    id_refunds = models.ForeignKey(
        Refund,
        verbose_name="ID del reembolso",
        on_delete=models.CASCADE
    )
    id_cat = models.ForeignKey(
        Category,
        verbose_name="ID de la categoria",
        on_delete=models.CASCADE
    )
    id_terminal = models.ForeignKey(
        Terminal,
        verbose_name="ID de la terminal",
        on_delete=models.CASCADE
    )
    id_cashout = models.ForeignKey(
        CashoutM,
        verbose_name="ID del retiro",
        on_delete=models.CASCADE
    )

    def __str__(self):
        txt = "ID: {} / QR ID: {}"
        return txt.format(self.id_ticket, self.id_qr)
