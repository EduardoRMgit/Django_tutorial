from django.db import models
from dapp.models import Merchant
from dapp.models import Category


class UbicacionT(models.Model):
    class Meta:
        verbose_name_plural = "Ubicacion de la tienda"

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

    def __str__(self):
        txt = "ID MER:{} / ID CAT: {} "
        return txt.format(self.id_mer, self.id_cat)
