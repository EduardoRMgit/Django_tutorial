from cactus.schema import schema
from django.contrib.auth import get_user_model
from django.test import Client
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.core.management import call_command
from ..perms import load_groups
from django.contrib.auth import authenticate
from django.http import HttpRequest


class TestNewUserReferencia(JSONWebTokenTestCase):

    GRAPHQL_SCHEMA = schema

    def setUp(self):
        call_command('loaddata', 'customer', verbosity=0)
        call_command('loaddata', 'adminUtils', verbosity=0)
        load_groups()
        call_command('loaddata', 'urls', verbosity=0)
        call_command('loaddata', 'user', verbosity=0)
        call_command('loaddata', 'statusRegistro', verbosity=0)
        call_command('loaddata', 'codigoconfianza', verbosity=0)

        self._client = Client()
        self.user = get_user_model().objects.get(username='test')
        self._pass = "12345678"
        request = HttpRequest()
        authenticate(request,
            username=self.user,
            password=self._pass)

    def test_create_user_codref(self):
        """Prueba la creación de usuario con contraseña y codigo de
        referencia."""

        mutation = '''
        mutation CreateUser($username: String!, $password: String!,
                            $codigoReferencia: String!) {
                createUser(
                    username: $username,
                    password: $password,
                    codigoReferencia: $codigoReferencia,
                        ){
                    user{
                        username
                    }
                    codigoconfianza{
                        codigoReferencia
                    }
                 }
        }
        '''
        variables = {'username': 'testname',
                     'password': 'testpass',
                     'codigoReferencia': '1234567890123456'}
        res = self.client.execute(mutation, variables)
        expected_res = {
            'createUser': {
                'user': {
                    'username': 'testname',
                },
                'codigoconfianza': {
                    'codigoReferencia': '1234567890123456',
                }
            }
        }
        self.assertEqual(res.data, expected_res)
        print("    [assert OK] User with reference code, created!")

    def test_ref_no_valida(self):
        """Prueba que se valide de forma correcta con respecto al contenido de
        entidades"""

        mutation = '''
        mutation CreateUser($username: String!, $password: String!,
                            $codigoReferencia: String!) {
                createUser(
                    username: $username,
                    password: $password,
                    codigoReferencia: $codigoReferencia,
                    ){
                    user{
                        username
                    }
                    codigoconfianza{
                        codigoReferencia
                    }
                 }
        }
        '''
        variables = {'username': 'testname03',
                     'password': 'testpass03',
                     'codigoReferencia': '1234567890'}
        res = self.client.execute(mutation, variables)
        self.assertEqual(res.errors[0].message,
                         'Codigo de referencia invalido')
        print("    [assert OK] Invalid ref code")

    def test_create_user_no_pass(self):
        """Prueba la no creación de usuarios sin contraseña al intentar
        registrarse para evitar la creación de usuarios con contraseñas
        NULL."""

        mutation = '''
        mutation CreateUser($username: String!,
            $codigoReferencia: String!) {
                createUser(
                    username: $username,
                    codigoReferencia: $codigoReferencia,
                ){
                    user{
                        username
                    }
                    codigoconfianza{
                        codigoReferencia
                    }
                 }
        }
        '''
        variables = {'username': 'testname04',
                     'codigoReferencia': '1234567890123456'}
        res = self.client.execute(mutation, variables)
        expected_res = {
            'createUser': {
                'user': None,
                'codigoconfianza': None,
            }
        }
        self.assertEqual(res.data, expected_res)
        print("    [assert OK] User not created 'cause <no password>")

    def test_existing_user(self):
        """Valida la existencia del nombre de un usuario,
           en caso de ser asi no genera el usuario nuevo"""

        mutation = '''
        mutation CreateUser($username: String!,
            $codigoReferencia: String!) {
                createUser(
                    username: $username,
                    codigoReferencia: $codigoReferencia,
                ){
                    user{
                        username
                    }
                    codigoconfianza{
                        codigoReferencia
                    }
                 }
        }
        '''
        variables = {'username': 'Aldo',
                     'password': 'x3',
                     'codigoReferencia': '1234567890123456'}
        res = self.client.execute(mutation, variables)
        expected_res = {
            'createUser': {
                'user': None,
                'codigoconfianza': None
            }
        }
        self.assertEqual(res.data, expected_res)
        print("    [assert OK] Existing user")
