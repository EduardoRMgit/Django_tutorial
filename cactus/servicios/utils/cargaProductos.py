import requests
import json
import wget
import os
from django.core.files import File
from servicios.models import Productos, Logotypes, ImgRef


def listaProductos():
    # select URLs for local and live testing: authentication and products
    site = os.getenv("SITE", "local")
    if site == "local":
        url1 = 'http://127.0.0.1:8001/GPOApp/api-token-auth/'
        url2 = 'http://127.0.0.1:8001/GPOApp/products/'
    else:
        url1 = 'http://165.227.242.135/GPOApp/api-token-auth/'
        url2 = 'http://165.227.242.135/GPOApp/products/'

    print(url1)
    # hardcoded credentials for local server
    payload = {"username": "ernesto", "password": "x"}
    headers1 = {'content-type': 'application/json'}
    data = json.dumps(payload)

    # Requests authentication token and extracts from response
    try:
        r1 = requests.post(url1, data=data, headers=headers1)
        token = r1.json()['token']
    except Exception as e:
        raise Exception(f'Error while obtaining token (gpo): {e}')

    headers2 = {'content-type': 'application/json',
                'Authorization': f'Token {token}'
                }

    # Use get() to obtain a list of products
    try:
        r2 = requests.get(url2, headers=headers2)
        datos = r2.json()
    except Exception as e:
        raise Exception(f'Error while requesting products (gpo): {e}')

    # Delete existing products, logos and refs and create new ones
    Productos.objects.all().delete()
    Logotypes.objects.all().delete()
    ImgRef.objects.all().delete()

    # This loop uses wget() and create() for logos and refs
    for idx, product in enumerate(datos, start=1):

        url1 = 'https://gestopago.portalventas.net/sistema/'\
            'images/gestopago/servicios/'\
            '{}.png'.format(product['fields'].get('id_servicio'))

        url2 = 'https://gestopago.portalventas.net/sistema/'\
               'images/gestopago/referencias/'\
               '{}.jpg'.format(product['fields'].get('id_servicio'))
        # only used for flake8 purposes
        id_serv = product['fields'].get('id_servicio')
        try:
            if not Logotypes.objects.filter(id_servicio=id_serv).exists():
                logo = wget.download(url1)
                f = open(logo, 'rb')
                logP = Logotypes.objects.create(
                    Logo=File(f),
                    id_servicio=id_serv,
                    servicio=product['fields'].get('Servicio'))
                os.remove(logo)
            else:
                logP = Logotypes.objects.get(id_servicio=id_serv)
        except Exception:
            logP = None

        try:
            if not ImgRef.objects.filter(id_servicio=id_serv).exists():
                ref = wget.download(url2)
                g = open(ref, 'rb')
                imagen = ImgRef.objects.create(
                    Imagenes_referencia=File(g),
                    id_servicio=id_serv,
                    servicio=product['fields'].get('Servicio'))
                os.remove(ref)
            else:
                imagen = ImgRef.objects.get(id_servicio=id_serv)
        except Exception:
            imagen = None

        # Remove these fields from dict to pass **args to create()
        product['fields'].pop('logotypes')
        product['fields'].pop('imgref')
        Productos.objects.create(id=idx,
                                 logotypes=logP,
                                 imgref=imagen,
                                 **product['fields']
                                 )

    # Returns the new product count to display in admin site
    return (Productos.objects.all().count())
