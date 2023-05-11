from demograficos.models.comportamiento import (ComportamientoDiario,
                                                ComportamientoMensual)
from .models.regulacion import ValidacionRegulatoria
from .models.catalogos import CAMI
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models.transaccion import (Transaccion,
                                 StatusTrans,
                                 ValidacionSesion,
                                 ValidacionTransaccion)
import datetime
from graphql_jwt.utils import jwt_payload


@receiver(post_save, sender=Transaccion)
def create_panda(sender, instance, created, **kwargs):
    if created:
        date = datetime.date.today()
        payload = jwt_payload(instance.user)

        ValidacionSesion.objects.create(
            user=instance.user,
            transaccion=instance,
            epochExp=str(payload['exp']),
            epoxhOrigIat=str(payload['origIat']),
        )

        ValidacionTransaccion.objects.create(
            verificacion_db=True,
            verificacion_https=False,
            verificacion_intoto=True,
            transaccion=instance
        )

        comp = (ComportamientoDiario.objects.filter(user=instance.user)
                .filter(fecha=date))

        montoDay = float(instance.monto)
        if comp:
            comp = comp[0]
            montoDay += float(comp.monto)
            comp.numtrans += 1
            comp.monto = montoDay
            if comp.numtrans >= 3:
                comp.excesotransaccion = True

            comp.save()

        else:
            ComportamientoDiario.objects.create(
                monto=montoDay,
                numtrans=1,
                user=instance.user
            )

        camids = CAMI.objects.filter(tipo=0).order_by('monto')
        i = len(camids) - 1
        while (montoDay < camids[i].monto):
            i -= 1

        ValidacionRegulatoria.objects.create(
            alarma=False,
            idCAMID=camids[i],
            transaccion=instance

        )

        month = datetime.date.today().month
        montoMonth = float(instance.monto)
        camims = CAMI.objects.filter(tipo=1).order_by('monto')
        i = len(camims) - 1
        while (montoMonth < camims[i].monto):
            i -= 1

        comp = (ComportamientoMensual.objects.filter(user=instance.user)
                .filter(fecha__month=month))
        if comp:
            comp = comp[0]
            if (instance.monto * 2) >= comp.retiroMensualPromedio:
                comp.alarmaretiro = True
            montoMonth += float(comp.retiroMensualTotal)
            comp.retiroMensualTotal = montoMonth
            comp.numretiros += 1
            comp.retiroMensualPromedio = (comp.retiroMensualTotal /
                                          comp.numretiros)
            comp.save()

        else:
            ComportamientoMensual.objects.create(
                user=instance.user,
                retiroMensualTotal=montoMonth,
                numretiros=1,
                retiroMensualPromedio=montoMonth,
                montoInusualMensual=camims[i]
            )

        instance.statusTrans = (StatusTrans.objects
                                .filter(nombre='verificado'))[0]
        # stp_transaction_reviewed.send(sender=sender, transaccion=instance)
