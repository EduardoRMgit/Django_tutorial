from django.db import models
from django.contrib.auth.models import User


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


class ServicesArcus(models.Model):
    class Meta:
        verbose_name_plural = "Servicios Arcus"
    id_bill = models.IntegerField(
        primary_key=True)
    name = models.CharField(
        max_length=256, null=True, blank=True)
    biller_type = models.CharField(
        max_length=256, null=True, blank=True)
    bill_type = models.CharField(
        max_length=256, null=True, blank=True)
    country = models.CharField(
        max_length=256, null=True, blank=True)
    currency = models.CharField(
        max_length=256, null=True, blank=True)
    requires_name_on_account = models.BooleanField(
        null=True, blank=True)
    hours_to_fulfill = models.IntegerField(
        null=True, blank=True)
    account_number_digits = models.CharField(
        max_length=256, null=True, blank=True)
    mask = models.CharField(
        max_length=256, null=True, blank=True)
    can_check_balance = models.BooleanField(
        null=True, blank=True)
    supports_partial_payments = models.BooleanField(
        null=True, blank=True)
    has_xdata = models.BooleanField(
        null=True, blank=True)

    def __str__(self):
        return f"{self.id_bill}, {self.name}"


class RecargasArcus(models.Model):
    class Meta:
        verbose_name_plural = "Recargas Arcus"
    id_recarga = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    biller_type = models.CharField(max_length=256, null=True, blank=True)
    bill_type = models.CharField(max_length=256, null=True, blank=True)
    country = models.CharField(max_length=256, null=True, blank=True)
    currency = models.CharField(max_length=256, null=True, blank=True)
    requires_name_on_account = models.BooleanField(
        null=True, blank=True)
    hours_to_fulfill = models.IntegerField(
        null=True, blank=True)
    account_number_digits = models.CharField(
        max_length=256, null=True, blank=True)
    mask = models.CharField(max_length=256, null=True, blank=True)
    can_check_balance = models.BooleanField(
        null=True, blank=True)
    supports_partial_payments = models.BooleanField(
        null=True, blank=True)
    has_xdata = models.BooleanField(
        null=True, blank=True)
    available_topup_amounts = models.JSONField(
        null=True, blank=True)
    topup_commission = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.id_recarga}{self.name}"
