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
    elif SITE == 'prod':
        url_transaction = UrlsPLD.objects.get(nombre="movements")
        url_auth = UrlsPLD.objects.get(nombre="generateToken")
    else:
        url_transaction = UrlsPLD.objects.get(nombre="movements_sandbox")
        url_auth = UrlsPLD.objects.get(nombre="generateToken_sandbox")
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

        body = {
            'usr': cluster_secret('ubcubo-credentials', 'user'),
            'pass': cluster_secret('ubcubo-credentials', 'password'),
            'curp': trans.user.Uprofile.curp,
            'origen_pago': "aaaaaaaaaaaaaaaaaaaa",
            'tipo_cargo': "aaaaaaaaaaaaaaaaaaaa",
            'tipo_moneda': "MXN",
            'monto_pago': trans.monto,
            'fecha_pago': trans.fechaValor.strftime("%Y/%m/%d"),
            'cuenta': trans.user.Uprofile.cuentaClabe,
            'created_at': timezone.now().strftime("%Y/%m/%d"),
            'payment_made_by': "MC",
            'cuentaclabeB': trans.user.Uprofile.cuentaClabe,
            'cuentaclabeS': "aaaaaaaaaaaaaaaaaaaa",
            'concepto': trans.concepto,
            'usuario': trans.user.Ucustomer.no_cliente
        }

        headers = {
            'Accept': 'application/json',
            'X-API-KEY': cluster_secret('ubcubo-credentials', 'key'),
            'Authorization': token
        }

        res2 = requests.put(
            url=url_transaction,
            data=body,
            headers=headers
        )

        content_customer = json.loads(res2.content)

        Movimiento.objects.create(
            customer=trans.user.Ucustomer,
            transaccion=trans,
            curp=trans.user.Uprofile.curp,
            origen_pago="aaaaaaaaaaaaaaaaaaaa",
            tipo_cargo="aaaaaaaaaaaaaaaaaaaa",
            tipo_moneda="MXN",
            monto_pago=trans.monto,
            fecha_pago=trans.fechaValor("%Y/%m/%d"),
            cuenta=trans.user.Uprofile.cuentaClabe,
            created_at=timezone.now().strftime("%Y/%m/%d"),
            payment_made_by="MC",
            cuentaclabeB=trans.user.Uprofile.cuentaClabe,
            cuentaclabeS="aaaaaaaaaaaaaaaaaaaa",
            usuario_pld=trans.user.Ucustomer.no_cliente,
            concepto=trans.concepto
        )
        return content_customer
    except Exception as e:
        msg_pld = f"[Create Customer] Error al crear movement en ubcubo" \
                  f"para el usuario: {trans.user}"
        db_logger.warning(msg_pld, e)
        raise Exception(e)
