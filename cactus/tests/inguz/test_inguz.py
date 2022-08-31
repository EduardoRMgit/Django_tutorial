from ..testdb import load_min_test
from graphql_jwt.testcases import JSONWebTokenTestCase
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import get_user_model
from tests.perms import load_groups
from django.core.management import call_command


class TestInguzGraphQL(JSONWebTokenTestCase):

    def setUp(self):
        load_min_test()
        call_command('loaddata', 'user.json', verbosity=0)
        call_command('loaddata', 'contactos.json', verbosity=0)
        call_command('loaddata', 'contable_cuenta.json', verbosity=0)
        call_command('loaddata', 'cuenta_saldo.json', verbosity=0)
        call_command('loaddata', 'statusTrans.json', verbosity=0)
        call_command('loaddata', 'tipo_contable_cuenta.json', verbosity=0)

        load_groups()
        self.user = get_user_model().objects.get(username='test')
        self.token = get_token(self.user)

    def test_inguz(self):
        try:
            mutation = '''
                mutation createInguzTransaccion($token:String!,
                                                $concepto:String!,
                                                $abono:String!,
                                                $nip:String!,
                                                $contacto:Int!){
                                                    createInguzTransaccion(
                                                    token: $token,
                                                    concepto: $concepto,
                                                    abono: $abono,
                                                    nip: $nip,
                                                    contacto: $contacto){
                                                        inguzTransaccion{ id }  # noqa: E501
                                                        user { Uprofile { saldoCuenta } }   # noqa: E501
                        }
                    }
                '''
            variables = {
                'token': self.token,
                'concepto': "prueba",
                'abono': "0.0",
                'nip': "55287",
                'contacto': 1}

            self.client.execute(mutation, variables)
        except Exception as error:
            self.assertEqual(error, "El usuario no es cuenta inguz")
