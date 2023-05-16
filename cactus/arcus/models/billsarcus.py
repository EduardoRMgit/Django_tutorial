from django.db import models
from django.contrib.auth.models import User
from banca.models import Transaccion


class Bills(models.Model):
    class Meta:
        verbose_name_plural = "Bills"
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             related_name="user_bills")
    bill_id = models.IntegerField()
    account_number = models.CharField(max_length=100)
    monto = models.FloatField()

    def __str__(self):
        return self.user


class PagosArcus(models.Model):
    class Meta:
        verbose_name_plural = "Pagos arcus"
    transaccion = models.OneToOneField(Transaccion,
                                       on_delete=models.CASCADE,
                                       related_name="transaccion_recarga",
                                       blank=True,
                                       null=True)
    id_transaccion = models.CharField(max_length=2056, blank=True, null=True)
    tipo = models.CharField(max_length=256, blank=True, null=True)
    monto = models.FloatField(blank=True, null=True)
    moneda = models.CharField(max_length=20, blank=True, null=True)
    identificador = models.CharField(max_length=256, blank=True, null=True)
    comision = models.FloatField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    estatus = models.CharField(max_length=2056, blank=True, null=True)
    id_externo = models.CharField(max_length=2056, blank=True, null=True)
    descripcion = models.CharField(max_length=2056, blank=True, null=True)
    numero_telefono = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return f"{self.transaccion} {self.id_transaccion}"


class ServicesArcus(models.Model):
    class Meta:
        verbose_name_plural = "Servicios Arcus"
    sku_id = models.CharField(
            max_length=256, null=True, blank=True)
    name = models.CharField(
        max_length=256, null=True, blank=True)
    biller_type = models.CharField(
        max_length=256, null=True, blank=True)
    country = models.CharField(
        max_length=256, null=True, blank=True)
    bill_types = models.JSONField(
        max_length=4096, null=True, blank=True)
    currency = models.CharField(
        max_length=256, null=True, blank=True)
    customer_fee = models.FloatField(
        null=True, blank=True)
    customer_fee_type = models.CharField(
        max_length=256, null=True, blank=True)
    logo_url = models.URLField(
        max_length=4096, null=True, blank=True)
    autopay = models.BooleanField(
        null=True, blank=True)
    tracking = models.BooleanField(
        null=True, blank=True)
    supports_partial_payments = models.BooleanField(
        null=True, blank=True)
    hours_to_fulfill = models.IntegerField(
        null=True, blank=True)
    allows_reversal = models.BooleanField(
        null=True, blank=True)

    def __str__(self):
        return f"{self.sku_id}, {self.name}"


class RecargasArcus(models.Model):
    class Meta:
        verbose_name_plural = "Recargas Arcus"
    sku_id = models.CharField(
        max_length=256, null=True, blank=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    biller_type = models.CharField(max_length=256, null=True, blank=True)
    bill_type = models.CharField(max_length=256, null=True, blank=True)
    country = models.CharField(max_length=256, null=True, blank=True)
    currency = models.CharField(max_length=256, null=True, blank=True)
    customer_fee = models.FloatField(
        null=True, blank=True)
    customer_fee_type = models.CharField(
        max_length=256, null=True, blank=True)
    logo_url = models.URLField(
        max_length=4096, null=True, blank=True)
    mask = models.CharField(max_length=256, null=True, blank=True)
    topup_amounts = models.JSONField(
        null=True, blank=True)
    reference_lenght = models.CharField(
        max_length=256,
        null=True, blank=True)
    carrier = models.CharField(
        max_length=256,
        null=True, blank=True)

    def __str__(self):
        return f"{self.sku_id}{self.name}"
