from arcus.models import PagosArcus
from datetime import datetime, timedelta


def conciliacion_arcus_recargas():

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    pagos = PagosArcus.objects.filter(fecha_creacion__date=yesterday, tipo='R')
    if len(pagos) != 0:
        # Inicio del archivo
        header_date = today.strftime("%Y/%m/%d").replace('/', '')
        document = f"HEADER|{header_date}\n"
        for pago in pagos:
            monto = "{:.2f}".format(pago.monto)
            fecha = pago.fecha_creacion - timedelta(hours=5)
            fecha = fecha.strftime("%Y-%m-%dT%H:%M")
            register_line = f"REGISTER|{fecha}" \
                            f"|{pago.empresa_recargas.sku_id}" \
                            f"|{pago.id_transaccion}|{pago.numero_cuenta}" \
                            f"|{monto}|{pago.moneda}|{pago.id_externo}"
            document += f"{register_line}\n"
        register_count = len(pagos)

        document += f"FOOTER|{register_count}"
        with open(f"inguz_topups_mx_{header_date}.txt", "w") as file:
            file.write(document)

    else:
        header_date = today.strftime("%Y/%m/%d").replace('/', '')
        document = f"HEADER|{header_date}\n"
        document += "FOOTER|0"
        with open(f"inguz_topups_mx_{header_date}.txt", "w") as file:
            file.write(document)
