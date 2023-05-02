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
            statusTrans__nombre__in=["exito"]
        )
    valida_primera = transacciones.count()
    if valida_primera > 1:
        comisiones = ComisioneSTP.objects.all()
        for comision in comisiones:
            rango = (comision.rangotransacciones).split("-")
            if valida_primera >= int(
                    rango[0]) and valida_primera <= int(rango[1]):
                ivacliente = comision.ivaCliente
                ivastp = comision.ivaSTP
                cliente = comision.cliente
                stp = comision.stp
        monto = ivacliente + ivastp + cliente + stp
        return monto
    else:
        return monto
