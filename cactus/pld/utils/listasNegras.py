import requests
import json
from pld.models.urls import UrlsPLD


def listaNegra(data):
    # url = 'https://gt-servicios.com/propld/listsapi/searchlist'
    url = UrlsPLD.objects.get(id=4)

    headers = {
            'Accept': 'application/json',
            # 'X-API-KEY':'KYC-DSR92Sj2NgK8aPyPHXYSxjDs'
            'X-API-KEY': 'KYC-eWTR92Sj2NgK8aPyPHXYSxjVr'
    }

    r = requests.post(url, data=data, headers=headers)
    # k = json.loads(r.text)
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
