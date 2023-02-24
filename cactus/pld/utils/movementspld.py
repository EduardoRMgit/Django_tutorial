from pld.models import (Movimiento,
                        UrlsPLD)
import json
import requests
import logging
from cactus.utils import cluster_secret
from cactus.settings import SITE
from django.utils import timezone

db_logger = logging.getLogger('db')


def create_pld_movement(trans):

    if SITE == 'local':
        return

    if SITE == 'prod':
        url_transaction = UrlsPLD.objects.get(nombre="movements").urls
        url_auth = UrlsPLD.objects.get(nombre="generateToken").urls
    else:
        url_transaction = UrlsPLD.objects.get(nombre="movements_sandbox").urls
        url_auth = UrlsPLD.objects.get(nombre="generateToken_sandbox").urls
    try:
        headers_auth = {
            'Accept': 'application/json',
            'X-API-KEY': cluster_secret('ubcubo-credentials', 'key')
        }

        body_auth = {
            'usr': cluster_secret('ubcubo-credentials', 'user'),
            'pass': cluster_secret('ubcubo-credentials', 'password')
        }

        res = requests.post(
            url_auth,
            data=body_auth,
            headers=headers_auth
        )

        content = json.loads(res.content)
        token = content['token']

        if trans.tipoTrans.medio == "E":
            origen_pago = "01"  # From CNBV catalog
        elif trans.tipoTrans.medio == "T":
            origen_pago = "03"  # From CNBV catalog

        if trans.tipoTrans.tipo == "E":
            tipo_cargo = "01"
        elif trans.tipoTrans.tipo == "R":
            tipo_cargo = "02"

        body = {
            'usr': cluster_secret('ubcubo-credentials', 'user'),
            'pass': cluster_secret('ubcubo-credentials', 'password'),
            'curp': trans.user.Uprofile.curp,
            'origen_pago': origen_pago,
            'tipo_cargo': tipo_cargo,
            'tipo_moneda': "MXN",
            'monto_pago': trans.monto,
            'fecha_pago': trans.fechaValor.strftime("%Y/%m/%d"),
            'cuenta': trans.user.Uprofile.cuentaClabe,
            'created_at': timezone.now().strftime("%Y/%m/%d"),
            'payment_made_by': "MC",
            'concepto': trans.concepto,
        }

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-API-KEY': cluster_secret('ubcubo-credentials', 'key'),
            'Authorization': token
        }

        res2 = requests.put(
            url=url_transaction,
            data=body,
            headers=headers
        )

        content_movement = json.loads(res2.content)

        if res2.status_code != 200:
            db_logger.warning(
                f"[Create PLD Movement]: {trans.user} / {content_movement}"
            )
            return

        alerta = content_movement['response_api'][
            'alertas'] if content_movement[
                'response_api']['alertas'] else None

        if alerta:
            msg_pld = f"[ALERTAS PLD]: {alerta} para el usuario: {trans.user}"
            db_logger.info(msg_pld)

        Movimiento.objects.create(
            customer=trans.user.Ucustomer,
            transaccion=trans,
            curp=trans.user.Uprofile.curp,
            origen_pago=origen_pago,
            tipo_cargo=tipo_cargo,
            tipo_moneda="MXN",
            monto_pago=trans.monto,
            fecha_pago=trans.fechaValor,
            cuenta=trans.user.Uprofile.cuentaClabe,
            created_at=timezone.now(),
            payment_made_by="MC",
            concepto=trans.concepto,
            status_code=res2.status_code,
            mensaje=content_movement['response_api']['message'],
            alertas=alerta,
            response=content_movement
        )
    except Exception as e:
        msg_pld = "[Create Movement] Error al crear movement en ubcubo" \
                  f"para el usuario: {trans.user}"
        db_logger.warning(f"{msg_pld}:error {e}")
