from banca.models import ComisioneSTP
from datetime import datetime
from banca.models import Transaccion


def comisionSTP(instance):
    today = datetime.now()
    monto = instance.monto
    transacciones_d = Transaccion.objects.filter(
            tipoTrans__tipo="E",
            tipoTrans__medio="T",
            fechaValor__year=today.year,
            fechaValor__month=today.month,
            fechaValor__day=today.day,
            statusTrans__nombre__in=["exito"],
            user=instance.user
        )
    transacciones_t = Transaccion.objects.filter(
            tipoTrans__tipo="E",
            tipoTrans__medio="T",
            fechaValor__year=today.year,
            fechaValor__month=today.month,
        )
    valida_primera = transacciones_d.count()
    valida_total = transacciones_t.count()
    if valida_primera >= 1:
        comisiones = ComisioneSTP.objects.all()
        for comision in comisiones:
            if comision.rangotransacciones:
                rango = (comision.rangotransacciones).split("-")
                if valida_total >= int(
                        rango[0]) and valida_total <= int(rango[1]):
                    comision = ComisioneSTP.objects.get(
                        id=comision.id)
                    ivacliente = comision.ivaCliente
                    ivastp = comision.ivaSTP
                    cliente = comision.cliente
                    stp = comision.stp
                    _comision = comision
        monto = monto + ivacliente + ivastp + cliente + stp
        return monto, _comision
    else:
        return monto, None
