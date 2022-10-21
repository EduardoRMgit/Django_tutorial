from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class PaymentInfo(models.Model):

    class Meta:
        verbose_name = 'Información de cobro'
        verbose_name_plural = 'Información de cobros'

    qr = models.CharField(
        max_length=50,
        verbose_name="QR ID",
        null=False,
        blank=False
    )
    qr_description = models.CharField(
        max_length=200,
        verbose_name="Descripción del QR",
        null=True,
        blank=True
    )
    qr_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Monto del QR",
        validators=[
            MaxValueValidator(100000),
            MinValueValidator(0)
        ],
        null=True,
        blank=True
    )
    qr_currency = models.CharField(
        max_length=30,
        verbose_name="Mondeda de cambio del QR",
        null=True,
        blank=True
    )
    qr_reference_num = models.CharField(
        max_length=100,
        verbose_name="Referencia numérica del QR",
        null=True,
        blank=True
    )
    cashout_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Monto de retiro",
        validators=[
            MaxValueValidator(100000),
            MinValueValidator(0)
        ],
        null=True,
        blank=True
    )
    cashout_currency = models.CharField(
        max_length=50,
        verbose_name="Moneda de cambio del retiro",
        null=True,
        blank=True
    )

    merchant_name = models.CharField(
        max_length=100,
        verbose_name="Nombre de comercio",
        null=True,
        blank=True
    )
    merchant_address = models.CharField(
        max_length=100,
        verbose_name="Direccion de comercio",
        null=True,
        blank=True
    )
    merchant_image = models.CharField(
        max_length=50,
        verbose_name="Imagen de comercio",
        null=True,
        blank=True
    )
    merchant_type = models.IntegerField(
        verbose_name="Tipo de comercio",
        null=True,
        blank=True
    )
    category_id = models.CharField(
        max_length=50,
        verbose_name="ID de categoría",
        null=True,
        blank=True
    )
    category_name = models.CharField(
        max_length=50,
        verbose_name="Nombre de Categoría",
        null=True,
        blank=True
    )
    response = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self):
        txt = "qr: {} / monto: ${} "
        return txt.format(self.qr, self.qr_amount)


class Payments(models.Model):

    class Meta:
        verbose_name = 'Información de pago'
        verbose_name_plural = 'Información de pagos'

    payment_id = models.CharField(
        max_length=50,
        verbose_name="ID del pago",
        null=True,
        blank=True
    )
    payment_reference = models.CharField(
        max_length=200,
        verbose_name="Referencia del pago",
        null=True,
        blank=True
    )
    response = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self):
        txt = "id: {} / reference: {} "
        return txt.format(self.payment_id, self.payment_reference)


class StoreInfo(models.Model):

    class Meta:
        verbose_name = 'Información de ubicación de tienda'
        verbose_name_plural = 'Información de ubicación de tiendas'

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
    radius = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="radio"
    )
    response = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self):
        txt = "latitud: {} / longitud: {} "
        return txt.format(self.latitude, self.longitude)


class CreatePayment(models.Model):

    class Meta:
        verbose_name = 'Realizar un pago'
        verbose_name_plural = 'Realizar pagos'

    name = models.CharField(
        max_length=100,
        verbose_name="Nombre del cliente",
        null=True,
        blank=True
    )
    mail = models.EmailField(
        max_length=254,
        verbose_name="Email",
        null=True,
        blank=True
    )
    phone = models.CharField(
        max_length=13,
        verbose_name="Teléfono",
        null=True,
        blank=True
    )
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Monto del cobro",
        validators=[
            MaxValueValidator(100000),
            MinValueValidator(0)
        ],
        null=False,
        blank=False
    )
    cashout_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Monto de retiro",
        validators=[
            MaxValueValidator(100000),
            MinValueValidator(0)
        ],
        null=True,
        blank=True
    )
    code = models.CharField(
        max_length=50,
        verbose_name="code QR",
        null=False,
        blank=False
    )
    description = models.CharField(
        max_length=200,
        verbose_name="Descripción",
        null=False,
        blank=False
    )
    reference = models.CharField(
        max_length=200,
        verbose_name="Referencia",
        null=True,
        blank=True
    )
    response = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self):
        txt = "code: {} / amount: {} "
        return txt.format(self.code, self.amount)
