import os
import requests
import json

from base64 import b64encode
from OpenSSL import crypto


def generateSignatureDeleteSTP(user):
    import base64
    import environ

    from kubernetes import client, config

    env = environ.Env()
    STPSECRET = env.str('STPSECRET', '')
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        STP_KEY_PWD = v1.read_namespaced_secret(STPSECRET, 'default')
        STP_KEY_PWD = base64.b64decode(STP_KEY_PWD.data['key']).decode('utf-8')
    except Exception:
        STP_KEY_PWD = "12345678"
    baseString = (
        "||"
        "{empresa}"
        "|"
        "{cuenta}"
        "|"
        "{rfcCurp}"
        "||"
    ).format(empresa="ZYGOO",
             cuenta=user.Uprofile.cuentaClabe,
             rfcCurp=user.Uprofile.curp)

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


def delete_stp(user):

    site = os.getenv("SITE", "local")
    if site == "prod":
        url = 'https://prod.stpmex.com:7002/speiws/rest/cuentaModule/fisica'
    else:
        url = 'https://demo.stpmex.com:7024/speiws/rest/cuentaModule/fisica'

    signature = generateSignatureDeleteSTP(user)

    data = {"empresa": "ZYGOO",
            "firma": signature,
            "page": 0,
            "size": 500,
            "cuenta": user.Uprofile.cuentaClabe,
            "rfcCurp": user.Uprofile.curp}
    cert = os.path.join(
        os.path.dirname(__file__),
        "stpmex-com-chain.pem")
    resp = requests.delete(url,
                           json=data,
                           headers={"Content-Type": "application/json"},
                           verify=cert)
    id_ = json.loads(resp.content)['id']
    descripcion = json.loads(resp.content)['descripcion']
    return id_, descripcion
