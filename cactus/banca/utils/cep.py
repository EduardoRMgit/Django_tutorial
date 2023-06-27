import requests
from OpenSSL import crypto
from base64 import b64encode


def url_cep():
    stp_key_pwd = '12345678'
    stp_key_pwd = str.encode(stp_key_pwd)
    with open('stp-key-prueba.pem', 'r') as key:
        print(key)
        unlockedKey = crypto.load_privatekey(
            crypto.FILETYPE_PEM,
            key.read(),
            stp_key_pwd)
    empresa = "ZYGOO"
    tipo = "E"
    rastreo = "rexnrnaqdo"
    fecha = 20230626
    # fecha = transaccion.fecha

    cadena = f"||{empresa}|{rastreo}|{tipo}|{fecha}||"
    cadena = str.encode(cadena)
    firma = crypto.sign(unlockedKey, cadena, 'sha256')
    print(firma)
    firma = b64encode(cadena)
    firma = firma.decode("utf-8")
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
    url = "https://efws-dev.stpmex.com/efws/API/consultaOrdenes"
    print(data)
    response = requests.post(url=url, data=data, headers=headers)
    print(response.__dict__)


url_cep()
