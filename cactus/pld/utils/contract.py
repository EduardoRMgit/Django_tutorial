import requests
import json
from pld.models.urls import UrlsPLD


def llamada2(request):
    url = UrlsPLD.objects.get(id=1)
    headers = {
        'Accept': 'application/json',
        'X-API-KEY': 'KYC-eWTR92Sj2NgK8aPyPHXYSxjVr'
    }

    r = request
    data = {
        'id_entidad': r.get('id_entidad'),
        'curp': r.get('curp'),  # LLaves UNIQUES
        # 'rfc': r.get('rfc'),  # LLaves UNIQUES
        'no_credito': r.get('no_credito'),
        'unidad_credito': r.get('unidad_credito'),
        'tipo_moneda': r.get('tipo_moneda'),
        'T1': r.get('T1'),  # total del contrato
        'T2': r.get('T2'),  # cuota por periodo determinado
        'T3': r.get('T3'),  # fecha inical
        'instrumento_monetario': r.get('instrumento_monetario'),  # tarjeta
        'canales_distribucion': r.get('canales_distribucion'),  # donde?
        'Estado': r.get('Estado')
    }

    r = requests.post(url, data=data, headers=headers)
    k = json.loads(r.content)
    try:
        msg = k['message']
    except Exception as ex:
        msg = 'fail'
        print("en la funcion llamada(): ", ex)
    return (msg, r.status_code)
