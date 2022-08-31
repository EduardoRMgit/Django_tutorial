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
        print("Transacción recibida: --->1")
        cuenta_clabe = instance.cuentaBeneficiario
        print("Transacción recibida: --->1.1")
        userP = UserProfile.objects.get(cuentaClabe=cuenta_clabe)
        print("Transacción recibida: --->1.2")
        user = userP.user
        print("Transacción recibida: --->1.3")
        instance.user = user
        print("Transacción recibida: --->1.4")
        status = StatusTrans.objects.get(nombre="esperando respuesta")
        print("Transacción recibida: --->2")
        main_trans = Transaccion.objects.create(
            user=user,
            fechaValor=instance.time,  # TODO: parse instance.fechaOperacion
            monto=float(instance.monto),
            statusTrans=status,
            tipoTrans=tipo,
            concepto=instance.concepto,
            claveRastreo=instance.claveRastreo
        )
        print("Transacción recibida: --->3")
        instance.transaccion = main_trans
        user.Uprofile.saldo_cuenta += float(instance.monto)
        user.Uprofile.save()
        print("Transacción recibida: --->4")
        instance.referenciaNumerica = gen_referencia_numerica({
            'id': instance.id,
            'tipoCuentaBeneficiario': instance.tipoCuentaBeneficiario,
            'tipoCuentaOrdenante': instance.tipoCuentaOrdenante
        })
        print("Transacción recibida: --->5")
        instance.balance = '0'
        # fecha = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        fecha = timezone.now().strftime('%Y%m%d')
        instance.fechaOperacion = fecha
        instance.save()
        db_logger.info(f"[STP sendabono] data (postsave): {instance.__dict__}")
        print("Transacción recibida: --->6")
#         status = StatusTrans.objects.get(nombre="esperando respuesta")
#         flagSTP = True

#         if(instance.user is None):
#             cuenta_clabe = instance.cuentaBeneficiario
#             try:
#                 userP = UserProfile.objects.get(cuentaClabe=cuenta_clabe)
#                 user = userP.user
#             except Exception:
#                 # Aqui no deberia de estar esto Hay que regresar un error
#                 user = User.objects.get(username='aldo')
#             instance.user = user
#             flagSTP = False
#         else:
#             user = instance.user
#             print(f"    [stp usuario]: {user}")

#         # __valida_empresa(instance, user)
#         # if instance.statusTrans in [4, 5, 6]:
#         #     status = StatusTrans.objects.get(nombre="rechazada")

#         main_trans = Transaccion.objects.create(
#             user=user,
#             fechaValor=instance.time,  # TODO: parse instance.fechaOperacion
#             monto=float(instance.monto),
#             statusTrans=status,
#             tipoTrans=tipo,
#             concepto=instance.concepto,
#             claveRastreo=instance.claveRastreo
#         )

#         instance.transaccion = main_trans
#         instance.save()

#         print("Antes del pago")
#         if instance.statusTrans == 0 and flagSTP:
#             """
#                 el statusTrans de main_trans es asignado por un reciever
#                 al verificar que cumple con todos los requisitos de seguridad

#                 el reciever responsable se llama create_panda, esta en
#                 banca.recievers
#             """

#             print("AL PAGO: ")

#             user.Uprofile.saldo_cuenta -= float(instance.monto)
#             user.Uprofile.save()
#             instance.referenciaNumerica = gen_referencia_numerica({
#                 'id': instance.id,
#                 'tipoCuentaBeneficiario': instance.tipoCuentaBeneficiario,
#                 'tipoCuentaOrdenante': instance.tipoCuentaOrdenante

#             })
#             instance.save()
#             instance.pago()
#             print("FIN PAGO")
