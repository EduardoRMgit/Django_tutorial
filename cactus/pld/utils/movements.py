import requests
import json
from pld.models.urls import UrlsPLD


def llamada(request):
    url = UrlsPLD.objects.get(id=3)
    headers = {
        'Accept': 'application/json',
        'X-API-KEY': 'KYC-eWTR92Sj2NgK8aPyPHXYSxjVr'
    }

    r = request
    data = {
        'id_entidad': r.get('id_entidad'),
        # Equivale al id contract de respuesta. no_credito
        'id_credito': r.get('id_credito'),
        'origen_pago': r.get('origen_pago'),
        'tipo_cargo': r.get('tipo_cargo'),
        'tipo_cargo_e': r.get('tipo_cargo_e'),
        'tipo_moneda': r.get('tipo_moneda'),
        'monto_pago': r.get('monto_pago'),
        'fecha_pago': r.get('fecha_pago'),
        'payment_made_by': r.get('payment_made_by')
    }

    r = requests.put(url, data=data, headers=headers)
    k = json.loads(r.content)
    try:
        msg = k['message']
    except Exception as ex:
        msg = k['mensaje']
        print("en la funcion llamada(): ", ex)
    return (msg, r.status_code)
