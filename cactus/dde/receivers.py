from django.dispatch import receiver
from django.db.models.signals import post_save
from .models.transaccion import TransaccionDDE


@receiver(post_save, sender=TransaccionDDE)
def create_transaccion(sender, instance, created, **kwargs):
    if created:
        try:
            user = instance.user
            up = user.Uprofile
            monto = float(instance.monto)
        except Exception as e:
            raise Exception(e)
        instance.status = 'OK'
        up.saldo_cuenta -= monto
        up.save()
