from django.db import models
from django.contrib.auth.models import User
# from banca.models.productos import Productos
from banca.models.transaccion import TipoAnual


class Fondeador(models.Model):
    """

    ``Attributes:``

    - Descripcion:

    - apMaterno = CharField(max_length=50)
    - RFC = CharField(max_length=15)
    - limiteMaximoDeFondeo = FloatField()
    - user = many to one to user models

    """
    apMaterno = models.CharField(max_length=50)
    RFC = models.CharField(max_length=15)
    # Cuanto tiene disponible para darnos
    limiteMaximoDeFondeo = models.FloatField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Fondeador',
    )

    def __str__(self):
        return self.RFC


class PagoFondeador(models.Model):
    """

    ``Attributes:``

    - Descripcion:
    - monto = FloatField()

    - fechaCreacion = models.DateTimeField(null=True)

    - fechaInicialDeFondeo = DateTimeField(null=True)

    - fechaFinalDeFondeo = DateTimeField(null=True)

    - generaInteresesDesde = BooleanField(default=True)
      fondeador = many to one to fondeador models
    - productos = many to one to productos models
    """
    # Pago completo que hace el fondeador para recibir intereses.
    monto = models.FloatField()
    # fecha de creacion del Registro
    fechaCreacion = models.DateTimeField(null=True)
    # cuando empiezan a correr los intereses
    fechaInicialDeFondeo = models.DateTimeField(null=True)
    # cuando acaban de correr lo intereses
    fechaFinalDeFondeo = models.DateTimeField(null=True)
    # Desde cuando genera intereses,
    # cuando deposita o cuando se registra el pago
    # True es desde que deposita
    generaInteresesDesde = models.BooleanField(default=True)
    fondeador = models.ForeignKey(
        Fondeador,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    # productos = models.ManyToManyField(
    #     Productos,
    #     through='Producto_Fondeador',
    # )

    def __str__(self):
        return self.fondeador.RFC


class Producto_Fondeador(models.Model):
    """

    ``Attributes:``

    - Descripcion:

    - monto = FloatField()

    - fechaCreacion = DateTimeField(null=True)
    - fechaInicialDeFondeo = DateTimeField(null=True)
    - fechaFinalDeFondeo = DateTimeField(null=True)
    - generaInteresesDesde = BooleanField(default=True)
    - producto = many to one to productos models
    - pago = many to one to PagoFondeador models

    """
    # Monto que le toca a cada producto de fondeo a partir del pago realizado.
    monto = models.FloatField()
    # fecha de creacion del Registro
    fechaCreacion = models.DateTimeField(null=True)
    # cuando empiezan a correr los intereses
    fechaInicialDeFondeo = models.DateTimeField(null=True)
    # cuando acaban de correr lo intereses
    fechaFinalDeFondeo = models.DateTimeField(null=True)
    # Desde cuando genera intereses, cuando deposita o cuando se registra
    # True es desde que deposita
    generaInteresesDesde = models.BooleanField(default=True)
    # producto = models.ForeignKey(
    #     Productos,
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True
    # )
    pago = models.ForeignKey(
        PagoFondeador,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )


class RetornoFondeador(models.Model):
    """

    ``Attributes:``

    - Descripcion:

    - fechaPago = DateTimeField(null=True)
    - monto = FloatField()
    - tasa_porcentajeAnualizado = FloatField()
    - tipoAnual = many to one to  tipoanual
    - productoFondeador = many to one to Producto Fondeador

    """
    # El retorno de inversion diario que tiene el fondeador en sus pagos.
    fechaPago = models.DateTimeField(null=True)
    monto = models.FloatField()
    tasa_porcentajeAnualizado = models.FloatField()
    tipoAnual = models.ForeignKey(
        TipoAnual,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    productoFondeador = models.ForeignKey(
        Producto_Fondeador,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.monto)
