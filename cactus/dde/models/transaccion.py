from django.db import models
from django.contrib.auth.models import User


class TransaccionDDE(models.Model):

    monto = models.CharField(max_length=64, null=True, blank=True)
    status = models.CharField(max_length=64, null=True, blank=True)
    fechaTrans = models.CharField(max_length=64, null=True, blank=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_transaccion_dde'
    )

    def __str__(self):
        return 'monto: {}, status: {}'.format(self.monto, self.status)
