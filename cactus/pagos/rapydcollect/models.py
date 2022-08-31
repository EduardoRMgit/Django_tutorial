from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from jsonfield import JSONField


class PaymentMethodsCountry (models.Model):

    status = models.CharField(max_length=50)
    operation_id = models.CharField(max_length=250)
    payment_type = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    category = models.CharField(max_length=100)
    country = CountryField()
    payment_flow_type = models.CharField(max_length=255)
    currencies = models.CharField(max_length=10)


class RequiredFields(models.Model):

    error_code = models.CharField(max_length=255)
    status = models.CharField(max_length=25)
    message = models.CharField(max_length=255)
    response_code = models.CharField(max_length=50)
    operation_id = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    typetype = models.CharField(max_length=50)
    regex = models.CharField(max_length=50)
    is_required = models.BooleanField()
    minimum_expiration_seconds = models.IntegerField()
    maximum_expiration_seconds = models.IntegerField()


class Payment(models.Model):

    user = models.ForeignKey(
           User,
           on_delete=models.CASCADE,
           related_name='user_payment',
           null=True
           )

    # STATUS
    error_code = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, blank=True)
    message = models.CharField(max_length=255, blank=True)
    response_code = models.CharField(max_length=255, blank=True)
    operation_id = models.CharField(max_length=255, blank=True)
    # DATA
    idPayment = models.CharField(max_length=255, blank=True)
    amount = models.IntegerField(null=True)
    is_partial = models.BooleanField(null=True, blank=True)
    currency_code = models.CharField(max_length=5)
    country_code = CountryField()
    statusData = models.CharField(max_length=5, blank=True)
    description = models.CharField(max_length=50)
    merchant_reference_id = models.CharField(max_length=255, blank=True)
    customer_token = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255, blank=True)
    # PAYMENT METHOD DATA (dentro de data)
    id_method = models.CharField(max_length=255, blank=True)
    type_methos = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=100, blank=True)
    metadata_payment = JSONField(blank=True)
    # image_payment
    expiration = models.IntegerField(null=True, blank=True)
    captured = models.BooleanField(null=True, blank=True)
    refunded = models.BooleanField(null=True, blank=True)
    refunded_amount = models.IntegerField(null=True, blank=True)
    receipt_email = models.CharField(max_length=50, blank=True)
    redirect_url = models.CharField(max_length=50, blank=True)
    complete_payment_url = models.CharField(max_length=50, blank=True)
    receipt_number = models.CharField(max_length=50, blank=True)
    flow_type_payment = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)
    statement_descriptor = models.CharField(max_length=255, blank=True)
    transaction_id = models.CharField(max_length=50, blank=True)
    created_at = models.IntegerField(null=True, blank=True)
    metadata = JSONField(blank=True)
    failure_code = models.CharField(max_length=50, blank=True)
    failure_message = models.CharField(max_length=255, blank=True)
    paid = models.BooleanField(null=True, blank=True)
    paid_at = models.IntegerField(null=True, blank=True)
    dispute = JSONField(blank=True)
    refunds = JSONField(blank=True)
    order = models.CharField(max_length=255, blank=True)
    outcome = JSONField(blank=True)
    visual_codes = JSONField(blank=True)
    # TEXTUAL CODES (dentro de data)
    textual_codes = JSONField(null=True, blank=True)
    # dentro de textual
    payCode = models.CharField(max_length=255, null=True, blank=True)
    instructions = JSONField(blank=True)
    ewallet_id = models.CharField(max_length=255, blank=True)
    ewallets = JSONField(blank=True)
    ewallets_id = models.CharField(max_length=255, blank=True)
    ewallets_amount = models.IntegerField(null=True, blank=True)
    ewallets_percent = models.IntegerField(null=True, blank=True)
    ewallets_refunded_amount = models.IntegerField(null=True, blank=True)
    payment_method_options = JSONField(blank=True)
    payment_method_type = models.CharField(max_length=255, blank=True)
    payment_method_type_category = models.CharField(max_length=100, blank=True)
    merchant_requested_currency = models.BooleanField(blank=True)
    merchant_requested_amount = models.BooleanField(blank=True)
    merchant_requested_currency = models.BooleanField(null=True, blank=True)
    merchant_requested_amount = models.BooleanField(null=True, blank=True)
    webhook_data = JSONField(blank=True)
    fechaPago = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    # Transaction_propagation
    monto = models.IntegerField(default=0, blank=True)
    tipoTrans = models.IntegerField(null=True, blank=True)
    concepto = models.CharField(max_length=250, blank=True, null=True)
    claveRastreoR = models.CharField(max_length=64, null=True, blank=True)


class PaymentRequiredFields(models.Model):
    banco = models.CharField(max_length=50)
    metodos = JSONField()


class Paises(models.Model):
    nombre = CountryField()
    disponible = models.BooleanField(default=False)

    def __str__(self):
        return str(self.nombre)


class MetodosdepagoPais(models.Model):
    pais = models.ForeignKey(Paises,
                             on_delete=models.CASCADE,
                             related_name='pais_pago')
    nombre = models.CharField(max_length=100, null=True, blank=True)
    activo = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class TestWebhook(models.Model):

    response = models.TextField(max_length=500,
                                null=True,
                                blank=True,
                                )


class MetodosdepagoUsuario(models.Model):
    user = models.ForeignKey(
           User,
           on_delete=models.CASCADE,
           related_name='user_paymethod',
           null=True
           )
    pais = models.ForeignKey(MetodosdepagoPais, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    activo = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
