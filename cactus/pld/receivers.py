from django.dispatch import receiver
from django.db.models.signals import post_save
# from pld.admin.adminUtils import adminUtils
from pld.models import (Customer,
                        CustomerD,
                        UrlsPLD,
                        )
from demograficos.models.userProfile import UserProfile
from django.core import serializers
import json
import requests


@receiver(post_save, sender=UserProfile)
def create_PLD_Customer(sender, instance, created, **kwargs):
    try:
        user = instance.user
        # admin_Util = adminUtils.objects.get(id=1)
        customer = CustomerD.objects.get(pk=1)
        # if not created:
        #     customer = user.Ucustomer
        url_customer = UrlsPLD.objects.get(pk=2)
        url_auth = UrlsPLD.objects.get(pk=5)

        # Autorizando
        headers_auth = {
            'Accept': 'application/json',
            'X-API-KEY': 'KYC-kmgO5JzyMYjty06Oqu1NIQV12Pyy'
        }

        # Primer request
        try:
            r = requests.post(
                url_auth, data={"id_entidad": 5500}, headers=headers_auth)
        except Exception:
            r = {}
        try:
            auth = json.loads(r.content)
        except Exception:
            auth = {}

        # Respuesta de request, seleccion de fixtures
        token = auth.get('token', -1)

        # Serializando Customer creado para enviar datos a UBCubo
        serialized = serializers.serialize('json', [customer, ])
        d = json.loads(serialized)[0]

        d['fields']['rfc'] = instance.rfc or customer.rfc
        d['fields']['curp'] = instance.curp or customer.curp
        d['fields']['amaterno'] = instance.apMaterno or customer.amaterno
        d['fields']['id_entidad'] = 5500
        d['fields']['genero'] = instance.sexo or customer.genero
        d['fields']['nombre'] = user.first_name or customer.nombre
        if instance.fecha_nacimiento:
            d['fields']['fecha_nacimiento'] = \
                instance.fecha_nacimiento.strftime("%Y-%m-%d") or \
                customer.fecha_nacimiento

        tels = user.user_telefono.filter(tipoTelefono_id__gte=0)
        if len(tels):
            tels_active = tels.filter(activo=True)
            if len(tels_active):
                tels = tels_active
            d['fields']['telefono_fijo'] = tels[0].telefono \
                or customer.telefono_fijo

        tels = user.user_telefono.filter(tipoTelefono_id=0)
        if len(tels):
            tels_active = tels.filter(activo=True)
            if len(tels_active):
                tels = tels_active
            d['fields']['telefono_movil'] = tels[0].telefono \
                or customer.telefono_movil

        d['fields']['correo_electronico'] = user.email or \
            customer.correo_electronico
        d['fields']['profesion'] = instance.ocupacion or customer.profesion

        dirs = user.user_direccion.all()
        if len(dirs):
            dirs2 = dirs.filter(activo=True)
            if len(dirs2):
                dirs = dirs2
            dir1 = dirs[0]

            d['fields']['calle'] = dir1.calle or customer.calle
            d['fields']['no_exterior'] = dir1.num_ext or customer.no_exterior
            d['fields']['no_interior'] = dir1.num_int or customer.no_interior
            d['fields']['cp'] = dir1.codPostal or customer.cp
            d['fields']['colonia'] = dir1.colonia or customer.colonia
            d['fields']['municipio'] = (dir1.delegMunicipio
                                        or customer.municipio)
            d['fields']['ciudad'] = dir1.ciudad or customer.ciudad
            d['fields']['estado_domicilio'] = dir1.entidadFed.entidad or \
                customer.estado_domicilio

        headers = {
            'Accept': 'application/json',
            'X-API-KEY': 'KYC-kmgO5JzyMYjty06Oqu1NIQV12Pyy',
            'Authorization': token
        }

        # Segundo request, autorizado
        try:
            r = requests.put(url_customer, data=d['fields'], headers=headers)
        except Exception as e:
            print('error doing request put: ', e)
            r = {}
        try:
            k = json.loads(r.content)
        except Exception as e:
            print('error reading json from resp put: ', e)
            k = {}

        res_api = k.get('response_api', {})
        msg = res_api.get('message', 'Inguz says: request failed')

        if 'IS ALREADY REGISTERED' in msg:
            # r_antes = r
            try:
                r = requests.post(url_customer, data=d['fields'],
                                  headers=headers)
            except Exception as e:
                print('error doing request post: ', e)
                r = {}
        try:
            k = json.loads(r.content)
        except Exception as e:
            print('error reading json from resp post: ', e)
            k = {}

        res_api = k.get('response_api', {})
        msg = res_api.get('message', 'Inguz says: request failed')
        id_no = res_api.get('id', -1)
        status = res_api.get('status', -1)

        d['fields']['mensaje'] = msg
        d['fields']['id_back'] = id_no
        d['fields']['status_code'] = status

        # Creacion de Customer a partir de User
        try:
            Customer.objects.update_or_create(
                user=user,
                defaults=d['fields']
            )
        except Exception as e:
            print("Error: ", e, "/n al crear Customer con Usuario: ", user)
    except Exception:
        pass
