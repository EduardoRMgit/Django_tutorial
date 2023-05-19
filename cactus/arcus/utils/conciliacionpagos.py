from arcus.models import PagosArcus
from datetime import datetime, timedelta


def conciliacion_arcus_pagos():

    today = datetime.now().date()
    pagos = PagosArcus.objects.filter(fecha_creacion__date=today, tipo='S')
    if len(pagos) != 0:
    # Inicio del archivo
        header_date = today.strftime("%Y/%m/%d").replace('/', '')
        document = f"HEADER|{header_date}\n"
        for pago in pagos:
            monto = "{:.2f}".format(pago.monto)
            fecha = pago.fecha_creacion - timedelta(hours=5)
            fecha = fecha.strftime("%Y-%m-%dT%H:%M")
            register_line = f"REGISTER|{fecha}" \
                            f"|{pago.empresa_servicio.sku_id}" \
                            f"|{pago.id_transaccion}|{pago.numero_cuenta}" \
                            f"|{monto}|{pago.moneda}|{pago.id_externo}"
            document += f"{register_line}\n"
        register_count = len(pagos)

        document += f"FOOTER|{register_count}"
        with open(f"chainname_{header_date}.txt", "w") as file:
            file.write(document)

    else:
        header_date = today.strftime("%Y/%m/%d").replace('/', '')
        document = f"HEADER|{header_date}\n"
        document += f"FOOTER|0"
        with open(f"chainname_{header_date}.txt", "w") as file:
            file.write(document)

conciliacion_arcus_pagos()
