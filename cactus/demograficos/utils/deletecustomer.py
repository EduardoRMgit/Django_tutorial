import json
import requests
import logging
from cactus.settings import cluster_secret

db_logger = logging.getLogger('db')


def pld_customer_delete(curp):

    url_customer = cluster_secret('ubcubo-credentials', 'urldeletecustomer')
    url_auth = cluster_secret('ubcubo-credentials', 'urltoken')

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
            url=url_auth,
            data=body_auth,
            headers=headers_auth
        )

        content = json.loads(res.content)
        token = content['token']

        body = {
            'usr': cluster_secret('ubcubo-credentials', 'user'),
            'pass': cluster_secret('ubcubo-credentials', 'password'),
            'customer': curp
        }

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-API-KEY': cluster_secret('ubcubo-credentials', 'key'),
            'Authorization': token
        }

        res2 = requests.post(
            url=url_customer,
            data=body,
            headers=headers
        )

        content_delete = json.loads(res2.content)

        db_logger.info(
            f"[Delete Customer]: {curp} request: {res2.request.__dict__}"
            f"response: {content_delete}"
        )

        if res2.status_code != 200:
            db_logger.warning(
                f"[Delete Customer]: Error en la respuesta {curp}"
            )

    except Exception as ex:
        msg_pld = f"[Delete Customer] Error al eliminar customer en ubcubo " \
                  f"para el usuario con curp {curp}. Error: {ex}"
        db_logger.warning(msg_pld)
