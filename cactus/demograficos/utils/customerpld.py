from pld.models import (Customer,
                        UrlsPLD)
import json
import requests


def create_pld_customer(user):
    try:
        url_customer = UrlsPLD.objects.get(pk=2)
        url_auth = UrlsPLD.objects.get(pk=5)

        headers_auth = {
            'Accept': 'application/json',
            'X-API-KEY': 'KYC-kmhwgO5hJzyMYjty06Oqu1NIQV1-2Pyy'
        }

        body_auth = {
            'usr': 'apiInvercratoSand',
            'pass': '258onttsR-3'
        }

        res = requests.post(
            url_auth,
            data=body_auth,
            headers=headers_auth
        )
        content = json.loads(res.content)
        token = content['token']
        print(token)
        body = {
            'usr': 'apiInvercratoSand',
            'pass': '258onttsR-3',
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
            'X-API-KEY': 'KYC-kmhwgO5hJzyMYjty06Oqu1NIQV1-2Pyy',
            'Authorization':  token
        }

        res2 = requests.put(
            url=url_customer,
            data=body,
            headers=headers
        )
        print(url_customer)
        content_customer = json.loads(res2.content)
        Customer.objects.create(
            id_entidad=5501,
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
            user=user
        )
        print(content_customer['response_api'])
    except Exception as e:
        print(e)
