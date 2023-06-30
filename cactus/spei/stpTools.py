import os
import requests
import json
import random
import string
import logging
import environ

from datetime import datetime

from OpenSSL import crypto

from base64 import b64encode

from datetime import timedelta, time


db_logger = logging.getLogger('db')


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

    db_logger.info(
        f"[STP generateSignatureString()] Cadena original: {baseString}")

    stp_key_pwd = str.encode(stp_key_pwd)
    with open('llavePrivada.pem', 'r') as key:
        # key = os.getenv('STP-PRIVATE-KEY')
        unlockedKey = crypto.load_privatekey(
            crypto.FILETYPE_PEM,
            key.read(),
            stp_key_pwd)

    baseString = str.encode(baseString)
    cipheredString = crypto.sign(unlockedKey, baseString, 'sha256')
    signatureString = b64encode(cipheredString)
    return signatureString


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def _set_fecha_operacion():
    hoy = datetime.now()
    fecha_nueva = hoy
    delta_horas = {
        1: 12,
        2: 12,
        3: 12,
        4: 12,
        5: 72,
        6: 48,
        7: 24
    }[hoy.isoweekday()]

    if hoy.isoweekday() in [6, 7] or hoy.time() >= time(18, 0):
        fecha_nueva = hoy + timedelta(hours=delta_horas)
        fecha_nueva = fecha_nueva.replace(hour=7, minute=0)

    return fecha_nueva.strftime('%Y%m%d')


def pago(data_pago):
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

    claveRastreo = data_pago['clave_rastreo']
    conceptoPago = data_pago['concepto_pago']
    cuentaBeneficiario = data_pago['cuenta_beneficiario']
    cuentaOrdenante = data_pago['cuenta_ordenante']
    empresa = "ZYGOO"
    folioOrigen = claveRastreo
    # institucionContraparte = '40002'
    institucionContraparte = data_pago['inst_contraparte']
    institucionOperante = "90646"
    monto = "{:.2f}".format(float(data_pago['monto']))
    nombreBeneficiario = data_pago['nombre_beneficiario']
    nombreOrdenante = data_pago['nombre_ordenante']
    referenciaNumerica = data_pago['referencia']
    rfcCurpBeneficiario = "ND"  # no disponible
    rfcCurpOrdenante = data_pago['rfc_curp_ordenante']  # "ND"  # no disponible
    tipoCuentaBeneficiario = "40"
    tipoCuentaOrdenante = "40"  # es 40 por cuenta clabe
    tipoPago = "1"  # tipo de pago 3 a 3

    fechaOperacion = _set_fecha_operacion()
    db_logger.info(f"[STP pago()] fechaOperacion: {str(fechaOperacion)}")

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

    site = os.getenv("SITE", "local")
    if site == "prod":
        url = 'https://prod.stpmex.com:7002/speiws/rest/ordenPago/registra'
    else:
        url = 'https://demo.stpmex.com:7024/speiws/rest/ordenPago/registra'
    db_logger.info(f"[STP pago()] URL ordenPago: {url}")

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

    db_logger_info = f"[STP ordenPago/registra] Request Data: {data}"
    db_logger.info(db_logger_info)

    try:
        cert = os.path.join(
            os.path.dirname(__file__),
            "stpmex-com-chain.pem")
        r = requests.put(url,
                         data=json.dumps(data),
                         headers=headers,
                         verify=cert)
        stpId = json.loads(r.text)['resultado']['id']
        resultado = json.loads(r.text)['resultado']
        db_logger.info(f"[STP ordenPago/registra] Response: {resultado}")
        stpMsg = "ID obtenido exitosamente"
        if 'descripcionError' in resultado:
            stpMsg = resultado['descripcionError']
        if stpId <= 0:
            db_logger.info(r.__dict__)

    except Exception as e:
        j = "{}{}{}".format(e, url, firma)
        db_logger.info(j)
        print("no nos quiere stp"+repr(e))
        db_logger.error("asssh"+repr(e))
        stpId = -1  # TODO revisar que id de error corresponde
        stpMsg = "no nos quiere stp"
        # al problema que contesta el servidor
    return [stpId, stpMsg]


def cadena_original_registro_cuenta(data):
    cadena_original = "||{}|{}|{}||".format(
        data['empresa'],
        data['cuenta'],
        data['rfcCurp']
    )
    msg = "{}{}".format("[(4) cadena_original_registro_cuenta]: ",
                        cadena_original)
    db_logger.info(msg)
    return cadena_original


def firma_cadena_registro_cuenta(data, stp_key_pwd):
    cadena_original = cadena_original_registro_cuenta(data)
    stp_key_pwd = str.encode(stp_key_pwd)
    with open('llavePrivada.pem', 'r') as key:
        unlockedKey = crypto.load_privatekey(
            crypto.FILETYPE_PEM,
            key.read(),
            stp_key_pwd)

    baseString = str.encode(cadena_original)
    cipheredString = crypto.sign(unlockedKey, baseString, 'sha256')
    firma = b64encode(cipheredString)
    return firma


def firma_consulta_cep(data, stp_key_pwd):
    cadena_original = data
    stp_key_pwd = str.encode(stp_key_pwd)
    with open('llavePrivada.pem', 'r') as key:
        # key = os.getenv('STP-PRIVATE-KEY')
        unlockedKey = crypto.load_privatekey(
            crypto.FILETYPE_PEM,
            key.read(),
            stp_key_pwd)

    baseString = str.encode(cadena_original)
    cipheredString = crypto.sign(unlockedKey, baseString, 'sha256')
    firma = b64encode(cipheredString)
    return firma


def registra_cuenta_persona_fisica(data):
    env = environ.Env()
    STPSECRET = env.str('STPSECRET', '')
    from kubernetes import client, config
    import base64
    try:
        config.load_kube_config()
    except Exception:
        config.load_incluster_config()
    v1 = client.CoreV1Api()
    STP_KEY_PWD = v1.read_namespaced_secret(STPSECRET, 'default')
    STP_KEY_PWD = base64.b64decode(STP_KEY_PWD.data['key']).decode('utf-8')

    data_registro = data
    firma = firma_cadena_registro_cuenta(data, STP_KEY_PWD)
    str_firma = firma.decode("utf-8")
    data_registro["firma"] = str_firma

    # TODO verificar URLs
    site = os.getenv("SITE", "local")
    if site == "prod":
        url = 'https://prod.stpmex.com:7002/speiws/rest/cuentaModule/fisica'
    else:
        url = 'https://demo.stpmex.com:7024/speiws/rest/cuentaModule/fisica'

    headers = {
        'Content-Type': 'application/json',
    }

    msg = f"[(5)] Data para registro de cuenta STP: {data}"
    db_logger.info(msg)

    try:
        cert = os.path.join(
            os.path.dirname(__file__),
            "stpmex-com-chain.pem")

        r = requests.put(url,
                         data=json.dumps(data),
                         headers=headers,
                         verify=cert)
        '''
        Respuesta esperada:
            {
                "descripcion": "",  (En caso de error (id>0) consultar
                                     el Catálogo de Respuesta Alta de Cuentas
                                     Personas Físicas para su validación)
                "id": 0  ( = 0 El proceso se ejecutó de manera correcta.
                           > 0 Ocurrió un error durante el procesamiento)
            }
        '''

        db_logger.info("respuesta STP: " + str(r.__dict__))
        _respuesta = json.loads(r.text)

        _id = _respuesta['id']
        _stp_descr = "Cuenta registrada exitosamente"
        if _id == 0:
            _stp_descr = _respuesta['descripcion']
            db_logger.info(str(r.__dict__))

    except Exception as ex:
        _log = "{}{}{}".format(ex, url, firma)
        db_logger.info(_log)
        db_logger.error(repr(ex))
        _id = -1
        _stp_descr = "Error en petición de registro de cuentas al WS"

    return [_id, _stp_descr]


def request_registra_persona_moral(cuenta_clabe):
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
        STP_KEY_PWD = str.encode("12345678")

    with open('llavePrivada.pem', 'r') as key:
        unlockedKey = crypto.load_privatekey(
            crypto.FILETYPE_PEM,
            key.read(),
            STP_KEY_PWD)

    cadena_original = f"||ZYGOO|{cuenta_clabe}|INV070903EY3||"
    msg = "{}{}".format("[registro_cuenta_persona_moral]: Cadena original",
                        cadena_original)
    db_logger.info(msg)
    cadena_original = crypto.sign(unlockedKey,
                                  str.encode(cadena_original),
                                  'sha256')
    firma = b64encode(cadena_original)
    data = {
        'nombre': "INVERCRATOS SAPI DE CV",
        'empresa': "ZYGOO",
        'cuenta': cuenta_clabe,
        'pais': "187",
        'rfcCurp': "INV070903EY3",
        'fechaConstitucion': "20070903",
        'entidadFederativa': "9",
        'actividadEconomica': "40",
        'firma': firma.decode("utf-8")
    }
    msg = f"[registro_cuenta_persona_moral] Data: {data}"
    db_logger.info(msg)
    try:
        site = os.getenv("SITE", "local")
        url = 'https://demo.stpmex.com:7024/speiws/rest/cuentaModule/moral'
        if site == "prod":
            url = 'https://prod.stpmex.com:7002/speiws/rest/cuentaModule/moral'

        cert = os.path.join(
            os.path.dirname(__file__),
            "stpmex-com-chain.pem")

        r = requests.put(url,
                         data=json.dumps(data),
                         headers={'Content-Type': 'application/json'},
                         verify=cert)
        db_logger.info(
            f"[registro_cuenta_persona_moral] respuestaSTP: {str(r.__dict__)}")
        respuesta = json.loads(r.text)
        return respuesta['id']

    except Exception as ex:
        db_logger.error(repr(ex))
        return -1


def registra_cuenta_persona_moral():

    from spei.models import FolioStp
    from spei.clabe import CuentaClabe
    from demograficos.models import UserProfile

    folio_stp = FolioStp.objects.last()
    folio = folio_stp.fol_dispatch()
    cuenta_clabe = CuentaClabe(folio)
    while UserProfile.objects.filter(
            cuentaClabe=cuenta_clabe).count() > 0:
        folio = folio_stp.fol_dispatch()
        cuenta_clabe = CuentaClabe(folio)

    id_resp = request_registra_persona_moral(cuenta_clabe)
    while id_resp == 3:
        folio = folio_stp.fol_dispatch()
        cuenta_clabe = CuentaClabe(folio)
        id_resp = request_registra_persona_moral(cuenta_clabe)

    return id_resp, cuenta_clabe


def gen_referencia_numerica(data):

    # Primer dígito del tipo de cuentaBeneficiario
    c_tipo_cuenta_benef = data['tipoCuentaBeneficiario'][-2:1]

    # Primer dígito del tipo de cuentaOrdenante
    c_tipo_cuenta_orden = data['tipoCuentaOrdenante'][-2:1]

    prefijo = f'{c_tipo_cuenta_benef}{c_tipo_cuenta_orden}'

    __id_trans = data['id']
    if __id_trans > 99999:
        __id_trans = str(__id_trans)[:-5]

    ref_num = f'{prefijo}{__id_trans:05}'
    return ref_num
