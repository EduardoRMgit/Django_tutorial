from django.db import models


class NivelCuenta(models.Model):
    class Meta():
        verbose_name_plural = 'Niveles de cuenta'

    NIVELES = (
        (1, "Nivel 1"),
        (3, "Nivel 3")
    )

    nivel = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        choices=NIVELES,
        verbose_name="Nivel de cuenta"
    )

    trans_mes = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Transferencias al mes"
    )

    saldo_max = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Saldo máximo"
    )

    dep_efectivo_mes = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Depósitos en efectivo al mes"
    )

    dep_efectivo_dia = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Depósitos en efectivo diario"
    )

    ret_efectivo_dia = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Retiro en efectivo diario"
    )

    def __str__(self):
        return ("Nivel " + str(self.nivel))
