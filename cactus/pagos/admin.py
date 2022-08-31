from django.contrib import admin
from pagos.rapydcollect.models import Payment


class PaymentRapyd(admin.StackedInline):
    model = Payment
    can_delete = False
    verbose_name_plural = 'Payment Rapyd'
    fk_name = 'payRapyd'


admin.site.register(Payment)
