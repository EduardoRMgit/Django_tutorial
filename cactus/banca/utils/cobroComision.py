from banca.models import ComisioneSTP
from datetime import datetime
from banca.models import Transaccion


def comisionSTP(instance):
    today = datetime.now()
    monto = instance.monto

    transacciones = Transaccion.objects.filter(
            tipoTrans__tipo="E",
            tipoTrans__medio="T",
            fechaValor__year=today.year,
            fechaValor__month=today.month,
            fechaValor__day=today.day,
            statusTrans__nombre__in=["exito"]
        )
    valida_primera = transacciones.count()
    if valida_primera > 1:
        comisiones = ComisioneSTP.objects.all()
        for comision in comisiones:
            (comision.rangotransacciones).split("-")
        monto = monto \
            + comision.ivaCliente \
            + comision.ivaSTP + comision.cliente + comision.stp
        return monto
    else:
        return monto
