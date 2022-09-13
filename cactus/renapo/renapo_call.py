import logging
from zeep import Client
from zeep.transports import Transport
import xml.etree.ElementTree as ET
from cactus.settings import RENAPO_USER, RENAPO_PASSWORD


def check_renapo(curp):

    db_logger = logging.getLogger('db')
    print("Esperando a RENAPO")
    transport = Transport()
    transport.session.verify = False
    try:
        client = Client('https://webs.curp.gob.mx/WebServicesConsulta/services/ConsultaPorCurpService?wsdl', transport=transport)   # noqa:E501

        datos_type = client.get_type('ns0:DatosConsultaCurp')

        datos = datos_type(tipoTransaccion=5,
                        cveCurp=curp,
                        usuario=RENAPO_USER,
                        password=RENAPO_PASSWORD)

        client.transport.session.verify = False

        mensaje = ""
        service = client.create_service('{http://services.wserv.ecurp.dgti.segob.gob.mx}ConsultaPorCurpServiceSoap12Binding',   # noqa:E501
                                        'https://webs.curp.gob.mx/WebServicesConsulta/services/ConsultaPorCurpService.ConsultaPorCurpServiceHttpSoap12Endpoint/')   # noqa:E501

        k = (service.consultarPorCurp(datos))
        r = ET.ElementTree(ET.fromstring(k)).getroot()
        json = r.attrib
        statusOper = json['statusOper']
        mensaje = json['message']

        if statusOper == 'EXITOSO' in json['statusOper']:
            nombres = (r[3].text)
            apellido1 = (r[1].text)
            apellido2 = (r[2].text)
            fechNac = (r[5].text)
            data = {}
            data['nombre_renapo'] = nombres
            data['ap_pat_renapo'] = apellido1
            data['ap_mat_renapo'] = apellido2
            data['fechNac_renapo'] = fechNac
            return data, mensaje
        elif mensaje == 'La CURP no se encuentra en la base de datos':
            mensaje = "[CONSULTA CURP RENAPO] Consulta exitosa, {}. \
            CURP INGRESADA: '{}'.".format(mensaje, curp)
            db_logger.error(mensaje)
            return False, mensaje
        else:
            return False, mensaje

    except Exception as ex:
        mensaje = "[CONSULTA CURP RENAPO] Falló la conexión a RENAPO al \
            intentar consultar curp: {}. Error: '{}'".format(curp, ex)
        db_logger.error(mensaje)
        return False, mensaje
