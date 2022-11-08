from django.db import models
from dapp.models import Qr
from dapp.models import Merchant
from dapp.models import Category
from dapp.models import CashoutM


class Info(models.Model):
    class Meta:
        verbose_name_plural = "Informacion del cobro"

    id_qr = models.ForeignKey(
        Qr,
        verbose_name="QR ID",
        on_delete=models.CASCADE
    )
    info = models.CharField(
        max_length=50,
        verbose_name="ID de la info",
        null=False,
        blank=False
    )
    id_mer = models.ForeignKey(
        Merchant,
        verbose_name="ID del comercio",
        on_delete=models.CASCADE
    )
    id_cat = models.ForeignKey(
        Category,
        verbose_name="ID de la categoria",
        on_delete=models.CASCADE
    )
    id_cash = models.ForeignKey(
        CashoutM,
        verbose_name="ID del retiro",
        on_delete=models.CASCADE
    )

    def __str__(self):
        txt = "id qr: {} / info: {}"
        return txt.format(self.id_qr, self.info)
