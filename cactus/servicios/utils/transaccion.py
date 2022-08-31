# import graphene
# from graphene_django.types import DjangoObjectType
# from servicios.models.transacciongpo import TransactionGpo
# from servicios.models.productos import Productos
# import requests
# import json
#
#
#
#
# def get_transaccion(self, request):
#     # Propiedades del request
#     data = {'id': id_servicio, 'Telefono': Telefono,
#             'Referencia': Referencia, 'Monto': Precio}
#     url = 'http://127.0.0.1:8000/GPOApp/transactions/'
#     url = 'http://167.99.25.139/GPOApp/transactions/'
#     headers = {'Accept': 'application/json',
#                'Authorization':
#                'Token 59ab64c13b4f99ca288c2d052486046d5575eee9'}
#
#     # Cuerpo del Request
#     r = requests.post(url, headers=headers, data=data)
#
