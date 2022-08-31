# -*- coding: utf-8 -*-
import json
from django.test import TestCase, Client
# from django.contrib.auth.models import User

# from rest_framework.test import APITestCase
# from rest_framework.test import APIClient

# from ..testdb import load_min_test
from django.core.management import call_command


class UsersTestCase(TestCase):

    def setUp(self):
        call_command('loaddata', 'customer', verbosity=0)
        call_command('loaddata', 'adminUtils', verbosity=0)
        call_command('loaddata', 'statusRegistro', verbosity=0)
        call_command('loaddata', 'errorestransaccion', verbosity=0)
        call_command('loaddata', 'urls', verbosity=0)
        self._client = Client()
        self._user1 = None
        self._user2 = None

    def test_create_first_user(self):
        username = "5551029634"
        mutation = """
            mutation{
                createUser(
                    username: "5551029634",
                    password: "Qwerty123456"
                    test: true
                ){
                    user{
                        username
                    }
                 }
            }
        """
        expected_res = {
            "createUser": {
                "user": {
                    "username": username
                }
            }
        }
        body = {
            'query': mutation,
            'operation_name': 'createUser'
        }
        res = self._client.post('/graphql', json.dumps(body),
                                content_type='application/json')
        jres = json.loads(res.content.decode())
        self.assertEqual(
            jres['data'],
            expected_res
        )
        # TODO CreateTelefono
        # self._user1 = User.objects.get(username=username)
        # pin = self._user1.user_telefono.last().PVTelefono.last().token
        # mutation = '''
        #   mutation{
        #     validacionTelefono(pin:"''' + pin + '''", numero:"5551029634")
        #       {
        #         validacion
        #       }
        #   }
        # '''
        # expected_res = {
        #     "validacionTelefono": {
        #         "validacion": "Validado"
        #     }
        # }
        # body = {
        #     'query': mutation,
        #     'operation_name': 'validacionTelefono'
        # }
        # print("    Validando primer Usuario...")
        # res = self._client.post('/graphql', json.dumps(body),
        #                         content_type='application/json')
        # jres = json.loads(res.content.decode())
        # self.assertEqual(
        #     jres['data'],
        #     expected_res
        # )
        # print("    [assert OK] Primer usuario (teléfono) validado")

    def test_create_second_user(self):
        username = "5551029635"
        mutation = """
            mutation{
                createUser(
                    username: "5551029635",
                    password: "Qwerty123456"
                    test: true
                ){
                    user{
                        username
                    }
                 }
            }
        """
        expected_res = {
            "createUser": {
                "user": {
                    "username": username
                }
            }
        }
        body = {
            'query': mutation,
            'operation_name': 'createUser'
        }
        res = self._client.post('/graphql', json.dumps(body),
                                content_type='application/json')
        jres = json.loads(res.content.decode())
        self.assertEqual(
            jres['data'],
            expected_res
        )
        # TODO CreateTelefono
        # self._user2 = User.objects.get(username=username)
        # pin = self._user2.user_telefono.last().PVTelefono.last().token
        # mutation = '''
        #   mutation{
        #     validacionTelefono(pin:"''' + pin + '''", numero:"5551029635")
        #       {
        #         validacion
        #       }
        #   }
        # '''
        # expected_res = {
        #     "validacionTelefono": {
        #         "validacion": "Validado"
        #     }
        # }
        # body = {
        #     'query': mutation,
        #     'operation_name': 'validacionTelefono'
        # }
        # print("    Validando segundo Usuario...")
        # res = self._client.post('/graphql', json.dumps(body),
        #                         content_type='application/json')
        # jres = json.loads(res.content.decode())
        # self.assertEqual(
        #     jres['data'],
        #     expected_res
        # )
        # print("    [assert OK] Segundo usuario (teléfono) validado")


# class TestSendAbono(APITestCase):

#     def setUp(self):
#         load_min_test()
#         call_command('loaddata', 'urls', verbosity=0)
#         call_command('loaddata', 'tipo_contable_cuenta', verbosity=0)
#         call_command('loaddata', 'contable_cuenta', verbosity=0)
#         call_command('loaddata', 'cuenta_saldo', verbosity=0)
#         call_command('loaddata', 'cuenta_tipo', verbosity=0)

#         self.transaccion_uri = "/api/sendabono/"
#         self.client = APIClient()

#     def test_post_transaccion(self):
#         profile = User.objects.get(
#             username="Zopi").Uprofile
#         profile.cuentaClabe = '646180190000000126'
#         profile.save()

#         data = {
#             "fechaOperacion": "20200122",
#             "institucionOrdenante": "BBVA",
#             "institucionBeneficiaria": "STP",
#             "claveRastreo": "123456",
#             "monto": "601.00",
#             "nombreOrdenante": "Alberto Almanza Rodríguez",
#             "tipoCuentaOrdenante": "40",
#             "cuentaOrdenante": "123456789087654321",
#             "rfcCurpOrdenante": "AAAAAAAAA",
#             "nombreBeneficiario": "Zopilote García",
#             "tipoCuentaBeneficiario": "40",
#             "cuentaBeneficiario": "646180190000000126",
#             "rfcCurpBeneficiario": "ZZZZZZZZZ",
#             "conceptoPago": "Helado de papaya",
#             "referenciaNumerica": "000001",
#             "empresa": "INVERCRATOS",
#             "tipoPago": 1,
#             "folioCodi": "666",
#             "tsLiquidacion": "666"
#         }
#         response = self.client.post(self.transaccion_uri, data)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(
#             User.objects.get(username="Zopi").Uprofile.cuentaClabe,
#             response.data.get('cuentaBeneficiario')
#         )
