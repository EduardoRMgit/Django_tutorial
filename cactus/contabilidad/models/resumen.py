from django.db import models
from django.utils import timezone


class AbstractComision(models.Model):
    """
    ``Attributes:``

    - Descripcion

    - saldoinicial = DecimalField(max_digits=30, decimal_places=4,
      null=True, blank=True)
    - debe = DecimalField(max_digits=30, decimal_places=4,
      null=True, blank=True)
    - haber = DecimalField(max_digits=30, decimal_places=4,
      null=True, blank=True)
    - saldofinal = DecimalField(max_digits=30, decimal_places=4,
      null=True, blank=True)
    - fecha = DateTimeField(default=timezone.now, null=True, blank=True)
    """
    saldoinicial = models.DecimalField(
        max_digits=30, decimal_places=4, null=True, blank=True)
    debe = models.DecimalField(
        max_digits=30, decimal_places=4, null=True, blank=True)
    haber = models.DecimalField(
        max_digits=30, decimal_places=4, null=True, blank=True)
    saldofinal = models.DecimalField(
        max_digits=30, decimal_places=4, null=True, blank=True)
    fecha = models.DateTimeField(
        default=timezone.now, null=True, blank=True)

    class Meta:
        abstract = True


class Resumen(AbstractComision):
    """
    ``Attributes:``

    - Descripcion

    - nombre = CharField(max_length=55)
    - codigo = CharField(max_length=30)
    - naturaleza = CharField(max_length=30)
    """
    nombre = models.CharField(max_length=55)
    codigo = models.CharField(max_length=30)
    naturaleza = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre


class CuentaPropia(AbstractComision):
    """
    ``Attributes:``

    - Descripcion

    - resumen = many to one to resesumen models
    """
    resumen = models.ForeignKey(
        Resumen,
        on_delete=models.CASCADE,
        related_name='cp_resumen'
    )


class SubcuentaIVA(AbstractComision):
    """
    ``Attributes:``

    - Descripcion

    - resumen = many to one to resesumen models
    """
    resumen = models.ForeignKey(
        Resumen,
        on_delete=models.CASCADE,
        related_name='sciva_resumen'
    )


class SubcuentaSTPIVA(AbstractComision):
    """
    ``Attributes:``

    - Descripcion

    - resumen = many to one to resesumen models
    """
    resumen = models.ForeignKey(
        Resumen,
        on_delete=models.CASCADE,
        related_name='scstpiva_resumen'
    )


class CuentaTerceros(AbstractComision):
    """
    ``Attributes:``

    - Descripcion:

    - resumen = many to one to resesumen models
    """
    resumen = models.ForeignKey(
        Resumen,
        on_delete=models.CASCADE,
        related_name='cterceros_resumen'
    )


class CuentaSTP(AbstractComision):
    """
    ``Attributes:``

    - Descripcion:

    - resumen = many to one to resesumen models
    """
    resumen = models.ForeignKey(
        Resumen,
        on_delete=models.CASCADE,
        related_name='cstp_resumen'
    )


class SCDTFTPE(AbstractComision):
    # SobregirosCuentasDerivadosTransmisionFondosPagoElectronico
    """
    ``Attributes:``

    - Descripcion:

    - resumen = many to one to resesumen models
    """
    resumen = models.ForeignKey(
        Resumen,
        on_delete=models.CASCADE,
        related_name='SCDTFTPE_resumen'
    )


class IVAacreditableNoPagado(AbstractComision):
    """
    ``Attributes:``

    - Descripcion:

    - resumen = many to one to resesumen models
    """
    resumen = models.ForeignKey(
        Resumen,
        on_delete=models.CASCADE,
        related_name='ivacrednop_resumen'
    )


class ComisionesporPagarSobreOperacionesVigentes(AbstractComision):
    """
    ``Attributes:``

    - Descripcion:

    - resumen = many to one to resesumen models
    """
    resumen = models.ForeignKey(
        Resumen,
        on_delete=models.CASCADE,
        related_name='copsov_resumen'
    )


class IVAnoCobrado(AbstractComision):
    """
    ``Attributes:``

    - Descripcion:

    - resumen = many to one to resesumen models
    """
    resumen = models.ForeignKey(
        Resumen,
        on_delete=models.CASCADE,
        related_name='ivanoco_resumen'
    )


class IVAcobrado(AbstractComision):
    """
    ``Attributes:``

    - Descripcion:

    - resumen = many to one to resesumen models
    """
    resumen = models.ForeignKey(
        Resumen,
        on_delete=models.CASCADE,
        related_name='ivaco_resumen'
    )


class ComisionesCobradas(AbstractComision):
    """
    ``Attributes:``

    - Descripcion:

    - resumen = many to one to resesumen models
    """
    resumen = models.ForeignKey(
        Resumen,
        on_delete=models.CASCADE,
        related_name='cocob_resumen'
    )


class ComisionesPagadas(AbstractComision):
    """
    ``Attributes:``

    - Descripcion:

    - resumen = many to one to resesumen models
    """
    resumen = models.ForeignKey(
        Resumen,
        on_delete=models.CASCADE,
        related_name='compa_resumen'
    )


class FondosPagoElectronico(AbstractComision):
    """
    ``Attributes:``

    - Descripcion:

    - resumen = many to one to resesumen models
    """
    resumen = models.ForeignKey(
        Resumen,
        on_delete=models.CASCADE,
        related_name='fpe_resumen'
    )
