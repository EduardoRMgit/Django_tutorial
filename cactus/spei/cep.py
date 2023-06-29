import requests
from spei.stpTools import firma_consulta_cep
import os
import json
from django.conf import settings
from datetime import datetime
import environ


def url_cep(transaccion):
    env = environ.Env()
    STPSECRET = env.str('STPSECRET', '')
    try:
        from kubernetes import client, config
        import base64
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        STP_KEY_PWD = v1.read_namespaced_secret(STPSECRET, 'default')
        STP_KEY_PWD = base64.b64decode(STP_KEY_PWD.data['key']).decode('utf-8')
    except Exception:
        STP_KEY_PWD = "12345678"
    empresa = transaccion.empresa
    tipo = transaccion.transaccion.tipoTrans.tipo
    rastreo = transaccion.claveRastreo
    fecha = datetime.strptime(transaccion.fechaOperacion, "%Y-%m-%d %H:%M:%S")
    fecha = datetime.strftime(fecha, "%Y%m%d")

    cadena = f"||{empresa}|{tipo}|{rastreo}|{fecha}||"
    firma = firma_consulta_cep(cadena, STP_KEY_PWD)
    firma = firma.decode("utf-8")
    cert = os.path.join(
        os.path.dirname(__file__),
        "stpmex-com-chain.pem")
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "claveRastreo": rastreo,
        "fechaOperacion": fecha,
        "empresa": empresa,
        "firma": firma,
        "tipoOrden": tipo,
    }
    url = settings.STP_CEP
    try:
        response = requests.post(url=url, data=json.dumps(data),
                                 headers=headers, verify=cert, timeout=5)
        response = json.loads(response.content.decode())
        url = response["datos"][0]["urlCEP"]
        print(response)
    except Exception:
        raise Exception(
            "No fue posible consultar la transacción, intente mas tarde.")
    return url
