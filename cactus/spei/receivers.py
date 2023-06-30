# import json
# import requests

# from datetime import datetime, timedelta
import logging

from notifications.signals import notify

from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from banca.models.catalogos import TipoTransaccion
from banca.models.transaccion import (Transaccion,
                                      StatusTrans)

from .models import StpTransaction
# from banca.signals import stp_transaction_reviewed
from demograficos.models import UserProfile

from .stpTools import gen_referencia_numerica


db_logger = logging.getLogger('db')


def notificacion_stp(sender, instance, created, **kwargs):
    if created:
        user = User.objects.all()
        notify.send(instance, verb='se hizo transaccion stp',
                    recipient=user)


post_save.connect(notificacion_stp, sender=StpTransaction)


@receiver(post_save, sender=StpTransaction)
def stp_transaction_propagation(sender, instance, created, **kwargs):

    if created and instance.user is None:

        db_logger.info(f"[STP sendabono] data(rcvd): {instance.__dict__}")

        # Tipo 1 (Transferencia recibida)
        tipo = TipoTransaccion.objects.get(codigo=1)
        cuenta_clabe = instance.cuentaBeneficiario
        userP = UserProfile.objects.get(cuentaClabe=cuenta_clabe)
        user = userP.user
        instance.user = user
        status = StatusTrans.objects.get(nombre="exito")
        main_trans = Transaccion.objects.create(
            user=user,
            fechaValor=instance.time,  # TODO: parse instance.fechaOperacion
            fechaAplicacion=instance.time,
            monto=float(instance.monto),
            statusTrans=status,
            tipoTrans=tipo,
            concepto=instance.concepto,
            claveRastreo=instance.claveRastreo
        )
        instance.transaccion = main_trans
        user.Uprofile.saldo_cuenta += float(instance.monto)
        user.Uprofile.save()
        instance.referenciaNumerica = gen_referencia_numerica({
            'id': instance.id,
            'tipoCuentaBeneficiario': instance.tipoCuentaBeneficiario,
            'tipoCuentaOrdenante': instance.tipoCuentaOrdenante
        })
        instance.balance = '0'
        # fecha = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        fecha = timezone.now().strftime('%Y%m%d')
        instance.fechaOperacion = fecha
        instance.save()
        db_logger.info(f"[STP sendabono] data (postsave): {instance.__dict__}")
