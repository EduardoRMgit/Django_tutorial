import requests
import json
import os
from OpenSSL import crypto
from base64 import b64encode

from django.utils import timezone

STP_CUENTA_CLABE = 40
STP_PAGO_3A3 = 1
STP_EMPRESA = 'INVERCRATOS'
STP_INSTITUCION_OPERANTE = 90646

# URL del archivo WSDL de STP
# STP_WSDL_URL =
# 'http://demo.stpmex.com:7004/speidemo/webservices/SpeiServices?wsdl'

# Ruta de la llave de encripcion para STP
# STP_KEY_PATH = os.path.join(BASE_DIR, 'stp-key-prueba.pem')
STP_KEY_PWD = '12345678'

claveRastreo = "12345670"
conceptoPago = "Pruebas Invercratos u"
cuentaBeneficiario = "846180000400000001"
cuentaOrdenante = "646180190012345675"
empresa = "INVERCRATOS"
folioOrigen = "000001"
# institucionContraparte = '40002'
institucionContraparte = '846'
institucionOperante = "90646"
monto = "123.45"
nombreBeneficiario = "David Fernandez"
nombreOrdenante = "Eduardo Martinez"
referenciaNumerica = "1234567"
rfcCurpBeneficiario = "ND"  # no disponible
rfcCurpOrdenante = "ND"  # no disponible
tipoCuentaBeneficiario = "40"
tipoCuentaOrdenante = "40"  # es 40 por cuenta clabe
tipoPago = "1"  # tipo de pago 3 a 3


def generateSignatureString(institucionContraparte,
                            empresa,
                            fechaOperacion,
                            folioOrigen,
                            claveRastreo,
                            institucionOperante,
                            monto,
                            tipoPago,
                            tipoCuentaOrdenante,
                            nombreOrdenante,
                            cuentaOrdenante,
                            rfcCurpOrdenante,
                            tipoCuentaBeneficiario,
                            nombreBeneficiario,
                            cuentaBeneficiario,
                            rfcCurpBeneficiario,
                            conceptoPago,
                            referenciaNumerica,
                            stp_key_pwd):

    baseString = (
        "||"
        "{iContraparte}"
        "|"
        "{fOperacion}"
        "|"
        "{empr}"
        "|"
        "{fOrigen}"
        "|"
        "{cRastreo}"
        "|"
        "{iOperante}"
        "|"
        "{monto}"
        "|"
        "{tPago}"
        "|"
        "{tCordenante}"
        "|"
        "{nOrdenante}"
        "|"
        "{cOrdenante}"
        "|"
        "{rfcCurpOrdenante}"
        "|"
        "{tipoCuentaBeneficiario}"
        "|"
        "{nBeneficiario}"
        "|"
        "{cBeneficiario}"
        "|"
        "{rfcCurpBeneficiario}"
        "||||||"
        "{concepto}"
        "||||||"
        "{rNumerica}"
        "||||||"
        "||"
    ).format(
        iContraparte=institucionContraparte,  # 1
        empr=empresa,  # 2
        fOperacion=fechaOperacion,  # 3
        fOrigen=folioOrigen,  # 4
        cRastreo=claveRastreo,  # 5
        iOperante=institucionOperante,  # 6
        monto=monto,  # 7
        tPago=tipoPago,  # 8
        tCordenante=tipoCuentaOrdenante,  # 9
        nOrdenante=nombreOrdenante,  # 10
        cOrdenante=cuentaOrdenante,  # 11
        rfcCurpOrdenante=rfcCurpOrdenante,  # 12
        tipoCuentaBeneficiario=tipoCuentaBeneficiario,  # 13
        nBeneficiario=nombreBeneficiario,  # 14
        cBeneficiario=cuentaBeneficiario,  # 15
        rfcCurpBeneficiario=rfcCurpBeneficiario,  # 16
        concepto=conceptoPago,  # 22
        rNumerica=referenciaNumerica   # 28
    )

    print('\nBASE STRING', baseString)
    stp_key_pwd = str.encode(stp_key_pwd)
    with open('stp-key-prueba.pem', 'r') as key:
        unlockedKey = crypto.load_privatekey(
            crypto.FILETYPE_PEM,
            key.read(),
            stp_key_pwd)

    baseString = str.encode(baseString)
    cipheredString = crypto.sign(unlockedKey, baseString, 'sha256')
    signatureString = b64encode(cipheredString)
    print('\nFIRMITA', signatureString)
    return signatureString


fecha = timezone.now().strftime('%Y%m%d')
fechaOperacion = fecha

firma = generateSignatureString(institucionContraparte,
                                fechaOperacion,
                                empresa,
                                folioOrigen,
                                claveRastreo,
                                institucionOperante,
                                monto,
                                tipoPago,
                                tipoCuentaOrdenante,
                                nombreOrdenante,
                                cuentaOrdenante,
                                rfcCurpOrdenante,
                                tipoCuentaBeneficiario,
                                nombreBeneficiario,
                                cuentaBeneficiario,
                                rfcCurpBeneficiario,
                                conceptoPago,
                                referenciaNumerica,
                                STP_KEY_PWD)

str_firma = firma.decode("utf-8")
print('\nFIRMAD', str_firma)

site = os.getenv("SITE", "local")
if site == "prod":
    url = 'http://prod.stpmex.com:7002/speiws/rest/ordenPago/registra'
else:
    url = 'https://demo.stpmex.com:7024/speiws/rest/ordenPago/registra'
headers = {
    'Content-Type': 'application/json',
}

data = {
    "claveRastreo": claveRastreo,
    "conceptoPago": conceptoPago,
    "cuentaBeneficiario": cuentaBeneficiario,
    "cuentaOrdenante": cuentaOrdenante,
    "empresa": empresa,
    "fechaOperacion": fechaOperacion,
    "folioOrigen": folioOrigen,
    "institucionContraparte": institucionContraparte,
    "institucionOperante": institucionOperante,
    "monto": monto,
    "nombreBeneficiario": nombreBeneficiario,
    "nombreOrdenante": nombreOrdenante,
    "referenciaNumerica": referenciaNumerica,
    "rfcCurpBeneficiario": rfcCurpBeneficiario,  # no disponible
    "rfcCurpOrdenante": rfcCurpOrdenante,  # no disponible
    "tipoCuentaBeneficiario": tipoCuentaBeneficiario,
    "tipoCuentaOrdenante": tipoCuentaOrdenante,  # es 40 por cuenta clabe
    "tipoPago": tipoPago,  # tipo de pago 3 a 3
    "firma": str_firma
}

print('\nURL', url)
print('\nDATA', data)

print('\n', data)

r = requests.put(url, data=json.dumps(data), headers=headers, verify=False)

print('\n')
print(r.text)
