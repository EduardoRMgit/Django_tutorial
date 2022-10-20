from django.db import models


class Merchant(models.Model):

    class Meta:
        verbose_name_plural = "Comercio"

    merchant = models.CharField(
        max_length=50,
        verbose_name="ID Comercio",
        null=False,
        blank=False
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Nombre",
        null=True,
        blank=True
    )
    address = models.CharField(
        max_length=100,
        verbose_name="Direccion",
        null=False,
        blank=False
    )
    image = models.CharField(
        max_length=50,
        verbose_name="Imagen",
        null=False,
        blank=False
    )
    latitude = models.DecimalField(
        max_digits=17,
        decimal_places=14,
        verbose_name="Latitud",
        null=False,
        blank=False
    )
    longitude = models.DecimalField(
        max_digits=17,
        decimal_places=14,
        verbose_name="Longitud",
        null=False,
        blank=False
    )
    phone = models.CharField(
        max_length=11,
        verbose_name="Telefono",
        null=False,
        blank=False
    )
    type = models.IntegerField(
        verbose_name="Tipo",
        null=False,
        blank=False
    )

    def __str__(self):
        txt = "ID: {} / Nombre: ${} "
        return txt.format(self.merchant, self.name)
