import logging
import requests
import json
from pld.models.urls import UrlsPLD


db_logger = logging.getLogger('db')


def get_token():
    url = 'https://gt-servicios.com/propld/keys/generateToken'
    headers = {
        'Accept': 'application/json',
        'X-API-KEY': 'KYC-kmgO5JzyMYjty06Oqu1NIQV12Pyy',
    }
    body = {
        'id_entidad': 5500
    }

    res = requests.post(
        url,
        data=body,
        headers=headers
    )

    content = json.loads(res.content)
    return content['token']


def listaNegra(data):
    url = "https://gt-servicios.com/prolistas/busquedaapi/searchperson"
    token = get_token()
    headers = {
        'Accept': 'application/json',
        'X-API-KEY': 'KYC-kmgO5JzyMYjty06Oqu1NIQV12Pyy',
        'Authorization': token
    }

    r = requests.post(url, data=data, headers=headers)
    k = json.loads(r.text)
    print("listaNegra: ", k)
    db_logger.info(
        f"[STP listaNegra()] response: {k}")

    try:
        k = json.loads(r.text)
        result = k.get('results')
    except Exception:
        result = False
        k = {}

    # print(json.dumps(k, sort_keys=True,
    #                 indent=4, separators=(',', ': ')))

    if not result:
        return ([k, 'O'])

    validacion = result[-1].get('tipo')

    if validacion == 'LISTA NEGRA' or validacion == 'BLOQUEADO':
        return ([k, 'N'])

    if validacion == 'PEP':
        return ([k, 'P'])

    # print('estado desconocido')
    return ([k, 'O'])
