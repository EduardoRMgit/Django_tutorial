from pld.models import (Customer,
                        UrlsPLD)
import json
import requests
import logging
from cactus.utils import cluster_secret
from cactus.settings import SITE

db_logger = logging.getLogger('db')


def create_pld_customer(user):
    if SITE == 'local':
        return
    elif SITE == 'prod':
        url_customer = UrlsPLD.objects.get(nombre="customer").urls
        url_auth = UrlsPLD.objects.get(nombre="generateToken").urls
    else:
        url_customer = UrlsPLD.objects.get(nombre="customer_sandbox").urls
        url_auth = UrlsPLD.objects.get(nombre="generateToken_sandbox").urls
    try:
        headers_auth = {
            'Accept': 'application/json',
            'X-API-KEY': cluster_secret('ubcubo-credentials', 'key')
        }

        body_auth = {
            'usr': cluster_secret('ubcubo-credentials', 'user'),
            'pass': cluster_secret('ubcubo-credentials', 'password')
        }

        res = requests.post(
            url_auth,
            data=body_auth,
            headers=headers_auth
        )

        content = json.loads(res.content)
        token = content['token']

        body = {
            'usr': cluster_secret('ubcubo-credentials', 'user'),
            'pass': cluster_secret('ubcubo-credentials', 'password'),
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
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-API-KEY': cluster_secret('ubcubo-credentials', 'key'),
            'Authorization': token
        }

        res2 = requests.put(
            url=url_customer,
            data=body,
            headers=headers
        )
        content_customer = json.loads(res2.content)


        db_logger.info(
            f"[Create Customer]: {user} request: {res2.request.__dict__}" \
            f"response: {content_customer}"
        )

        if res2.status_code != 200:
            db_logger.warning(
                f"[Create Customer]: Error en la respuesta {user}"
            )
            return

        if not content_customer['response_api']['message'] == \
                            'THE CURP IS ALREADY REGISTERED':
            Customer.objects.create(
                id_entidad=cluster_secret('ubcubo-credentials', 'entity'),
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
    except Exception as e:
        msg_pld = f"[Create Customer] Error al crear customer en ubcubo" \
                  f"para el usuario: {user}. Error: {e}"
        db_logger.warning(msg_pld)
