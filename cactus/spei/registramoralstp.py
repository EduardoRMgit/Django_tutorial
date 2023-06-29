import os
import requests
import json
import environ
from spei.stpTools import firma_cadena_registro_cuenta_moral
from spei.clabe import CuentaClabe
from spei.models import FolioStp


def registra_moral_stp():
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
    url = """https://stpmex.zendesk.com/hc/es/articles/
             360054436671-Registro-de-Cuentas-de-Personas-Morales"""
    cert = os.path.join(
           os.path.dirname(__file__),
           "stpmex-com-chain.pem")
    folio_stp = FolioStp.objects.last()
    cuenta_clabe = CuentaClabe(folio_stp.fol_dispatch())
    data = f"||ZYGOO|{cuenta_clabe}|INV070903EY3||"
    firma = firma_cadena_registro_cuenta_moral(data, STP_KEY_PWD).decode(
        "utf-8")
    data = {
        'nombre': "INVERCRATOS SAPI DE CV",
        'empresa': "ZYGOO",
        'cuenta': cuenta_clabe,
        'pais': "187",
        'rfcCurp': "INV070903EY3",
        'fechaConstitucion': "20070903",
        'entidadFederativa': "9",
        'actividadEconomica': "38",
        'firma': firma
        }
    resp = requests.put(url,
                        data=json.dumps(data),
                        headers={"Content-Type": "application/json"},
                        verify=cert)
    return resp
