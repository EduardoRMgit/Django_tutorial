from spei.models import ConciliacionSTP, StpTransaction

from django.utils import timezone

import os
import requests
import json

from base64 import b64encode
from OpenSSL import crypto

from datetime import timedelta, datetime


def generateSignatureConciliationSTP(tipo_orden_conciliacion, fecha):
    import base64
    import environ

    from kubernetes import client, config

    env = environ.Env()
    STPSECRET = env.str('STPSECRET', '')
    try:
        config.load_kube_config()
    except Exception:
        config.load_incluster_config()
    v1 = client.CoreV1Api()
    STP_KEY_PWD = v1.read_namespaced_secret(STPSECRET, 'default')
    STP_KEY_PWD = base64.b64decode(STP_KEY_PWD.data['key']).decode('utf-8')
    baseString = (
        "||"
        "{empresa}"
        "|"
        "{tipoOrden}"
        "|"
        "{fechaOperacion}"
        "||"
    ).format(empresa="ZYGOO",
             tipoOrden=tipo_orden_conciliacion,
             fechaOperacion=(fecha.strftime("%Y%m%d")))

    stp_key_pwd = str.encode(STP_KEY_PWD)
    with open('llavePrivada.pem', 'r') as key:
        unlockedKey = crypto.load_privatekey(
            crypto.FILETYPE_PEM,
            key.read(),
            stp_key_pwd)
    baseString = str.encode(baseString)
    cipheredString = crypto.sign(unlockedKey, baseString, 'sha256')
    signature = b64encode(cipheredString)
    signature = signature.decode("utf-8")
    return signature


def conciliacion_stp(objeto):
    from spei.models import MovimientoConciliacion

    url = "https://efws-dev.stpmex.com/efws/API/conciliacion"
    tipo_orden = str(objeto.tipo_orden_conciliacion)

    inicio = objeto.fecha_inicio
    fin = objeto.fecha_fin

    fechas = [
        inicio + timedelta(days=d) for d in range((fin - inicio).days + 1)]

    if (len(fechas)) > 32:
        mensaje = "El rango de fechas a consultar es demasiado amplio, \
            intente con máximo 1 mes."
        return mensaje

    for fecha in fechas:
        signature = generateSignatureConciliationSTP(
            tipo_orden, fecha)

        dia = fecha.strftime("%Y%m%d")
        data = {"empresa": "ZYGOO",
                "firma": signature,
                "page": 0,
                "size": 500,
                "tipoOrden": tipo_orden,
                "fechaOperacion": dia}
        cert = os.path.join(
            os.path.dirname(__file__),
            "stpmex-com-chain.pem")
        resp = requests.post(url,
                            data=json.dumps(data),
                            headers={"Content-Type": "application/json"},
                            verify=cert)
        c = json.loads(resp.content)
        status = resp.status_code
        mensaje = json.loads(resp.content)['mensaje']
        estado = json.loads(resp.content)['estado']
        if status == 200:
            conci = json.loads(resp.content)['datos']
            for c in conci:
                fecha = datetime.strptime(str(
                    c['fechaOperacion']), "%Y%m%d")
                trans = StpTransaction.objects.filter(stpId=str(c['idEF']))
                if trans:
                    trans.update(conciliado=True)
                    trans = trans.first()
                    estado = True
                else:
                    trans = None
                    estado = False

                try:
                    update = MovimientoConciliacion.objects.get(
                        idEF=c['idEF']
                    )
                    update.claveRastreo = c['claveRastreo']
                    update.conceptoPago = c['conceptoPago']
                    update.cuentaBeneficiario = c['cuentaBeneficiario']
                    update.cuentaOrdenante = c['cuentaOrdenante']
                    update.empresa = c['empresa']
                    update.estado = c['estado']
                    update.fechaOperacion = fecha
                    update.institucionContraparte = c['institucionContraparte']
                    update.institucionOperante = c['institucionOperante']
                    update.medioEntrega = c['medioEntrega']
                    update.monto = c['monto']
                    update.nombreBeneficiario = c['nombreBeneficiario']
                    update.nombreOrdenante = c['nombreOrdenante']
                    update.nombreCep = c['nombreCep']
                    update.rfcCep = c['rfcCep']
                    update.sello = c['sello']
                    update.rfcCurpBeneficiario = c['rfcCurpBeneficiario']
                    update.referenciaNumerica = c['referenciaNumerica']
                    update.rfcCurpOrdenante = c['rfcCurpOrdenante']
                    update.tipoCuentaBeneficiario = c['tipoCuentaBeneficiario']
                    update.tipoCuentaOrdenante = c['tipoCuentaOrdenante']
                    update.tipoPago = c['tipoPago']
                    update.tsCaptura = c['tsCaptura']
                    update.tsLiquidacion = c['tsLiquidacion']
                    update.causaDevolucion = c['causaDevolucion']
                    update.urlCEP = c['urlCEP']
                    update.conciliacion = objeto
                    update.stpTransaction = trans
                    update.conciliada = estado
                    update.save()

                except MovimientoConciliacion.DoesNotExist:
                    MovimientoConciliacion.objects.create(
                        idEF=c['idEF'],
                        claveRastreo=c['claveRastreo'],
                        conceptoPago=c['conceptoPago'],
                        cuentaBeneficiario=c['cuentaBeneficiario'],
                        cuentaOrdenante=c['cuentaOrdenante'],
                        empresa=c['empresa'],
                        estado=c['estado'],
                        fechaOperacion=fecha,
                        institucionContraparte=c['institucionContraparte'],
                        institucionOperante=c['institucionOperante'],
                        medioEntrega=c['medioEntrega'],
                        monto=c['monto'],
                        nombreBeneficiario=c['nombreBeneficiario'],
                        nombreOrdenante=c['nombreOrdenante'],
                        nombreCep=c['nombreCep'],
                        rfcCep=c['rfcCep'],
                        sello=c['sello'],
                        rfcCurpBeneficiario=c['rfcCurpBeneficiario'],
                        referenciaNumerica=c['referenciaNumerica'],
                        rfcCurpOrdenante=c['rfcCurpOrdenante'],
                        tipoCuentaBeneficiario=c['tipoCuentaBeneficiario'],
                        tipoCuentaOrdenante=c['tipoCuentaOrdenante'],
                        tipoPago=c['tipoPago'],
                        tsCaptura=c['tsCaptura'],
                        tsLiquidacion=c['tsLiquidacion'],
                        causaDevolucion=c['causaDevolucion'],
                        urlCEP=c['urlCEP'],
                        conciliacion=objeto,
                        stpTransaction=trans,
                        conciliada=estado
                    )
        if estado == 3:
            return (mensaje + " a STP, intente de nuevo en unos minutos o \
                mas tarde.")
    ConciliacionSTP.objects.filter(id=objeto.id).update(
        conciliado=True,
        hora_de_conciliacion=timezone.now())
