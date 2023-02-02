from pld.models import (Customer,
                        UrlsPLD)
from django.contrib.auth.models import User
import json
import requests


def create_pld_customer(user):
    try:
        u = User.objects.get(user=user)
        up = u.Uprofile
        url_customer = UrlsPLD.objects.get(pk=2)
        url_auth = UrlsPLD.objects.get(pk=5)

        headers_auth = {
            'Accept': 'application/json',
            'X-API-KEY': 'KYC-kmhwgO5hJzyMYjty06Oqu1NIQV1-2Pyy'
        }

        body_auth = {
            'usr': 'apiInvercratoSand'
            'pass': '258onttsR-3'
        }

        res = requests.post(
            url,
            data=body_auth,
            headers=headers_auth
        )
        content = json.loads(res.content)
        token = content['token']
        try:
            body = {
                'usr': 'apiInvercratoSand',
                'pass': '258onttsR-3',
                'tipo': 1,
                'aparterno': u.last_name,
                'amaterno': up.apMaterno,
                'nombre': u.first_name,
                'genero': up.sexo,
                'rfc': up.rfc,
                'curp': up.curp,
                'fecha_nacimiento': up.fecha_nacimiento.strftime("Y-%m-%d"),
                'nacionalidad':
            }

    except Exception:
        pass
