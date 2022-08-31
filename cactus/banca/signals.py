from django.dispatch import Signal


stp_transaction_reviewed = Signal(providing_args=['transaccion'])
