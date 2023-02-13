from pld.models import (Customer,
                        UrlsPLD)
import json
import requests
import logging
from cactus.settings import (UBCUBO_USER,
                             UBCUBO_PWD,
                             UBCUBO_KEY,
                             UBCUBO_ENTIDAD)


db_logger = logging.getLogger('db')


def create_pld_customer(user):
    try:
        url_customer = UrlsPLD.objects.get(pk=2)
        url_auth = UrlsPLD.objects.get(pk=5)

        headers_auth = {
            'Accept': 'application/json',
            'X-API-KEY': UBCUBO_KEY
        }

        body_auth = {
            'usr': UBCUBO_USER,
            'pass': UBCUBO_PWD
        }

        res = requests.post(
            url_auth,
            data=body_auth,
            headers=headers_auth
        )

        content = json.loads(res.content)
        token = content['token']

        body = {
            'usr': UBCUBO_USER,
            'pass': UBCUBO_PWD,
            'tipo': 1,
            'apaterno': user.last_name,
            'amaterno': user.Uprofile.apMaterno,
            'nombre': user.first_name,
            'genero': user.Uprofile.sexo,
            'rfc': user.Uprofile.rfc,
            'curp': user.Uprofile.curp,
            'fecha_nacimiento': user.Uprofile.fecha_nacimiento.strftime(
                "Y-%m-%d"),
            'nacionalidad': user.Uprofile.nacionalidad,
            'pais_nacimiento': user.Uprofile.nacionalidad,
            'actividad': user.Uprofile.ocupacion,
            'clabe': user.Uprofile.cuentaClabe,
            'correo_electronico': user.email,
        }

        headers = {
            'Accept': 'application/json',
            'X-API-KEY': UBCUBO_KEY,
            'Authorization':  token
        }

        res2 = requests.put(
            url=url_customer,
            data=body,
            headers=headers
        )

        content_customer = json.loads(res2.content)
        if content_customer['response_api']['message'] == \
                            'THE CURP IS ALREADY REGISTERED':
            pass
        else:
            Customer.objects.create(
                id_entidad=UBCUBO_ENTIDAD,
                tipo=1,
                apaterno=user.last_name,
                amaterno=user.Uprofile.apMaterno,
                nombre=user.first_name,
                genero=user.Uprofile.sexo,
                rfc=user.Uprofile.rfc,
                curp=user.Uprofile.curp,
                fecha_nacimiento=user.Uprofile.fecha_nacimiento,
                pais_nacimiento=user.Uprofile.nacionalidad,
                nacionalidad=user.Uprofile.nacionalidad,
                actividad=user.Uprofile.ocupacion,
                correo_electronico=user.email,
                actua_cuenta_propia=1,
                mensaje=content_customer['response_api']['message'],
                no_cliente=content_customer['response_api']['id'],
                riesgo=content_customer[
                    'response_api']['customer_info']['riesgo'],
                user=user,
                response=content_customer,
            )
            return content_customer
    except Exception as e:
        raise Exception(e)
        msg_pld = f"[Create Customer] Error al crear customer en ubcubo para" \
                  f"el usuario: {user}"
        db_logger.warning(msg_pld, e)
