
from cactus.schema import schema
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token
from django.test import Client
from graphql_jwt.testcases import JSONWebTokenTestCase
from ..testdb import load_min_test
from django.core.management import call_command
from django.contrib.auth import authenticate
from django.http import HttpRequest
from demograficos.models import Telefono


class DemograficosTestBase(JSONWebTokenTestCase):

    GRAPHQL_SCHEMA = schema

    def setUp(self):
        load_min_test()
        call_command('loaddata', 'entidadFed', verbosity=0)
        call_command('loaddata', 'tipoDireccion', verbosity=0)
        call_command('loaddata', 'direccion', verbosity=0)
        call_command('loaddata', 'component', verbosity=0)
        call_command('loaddata', 'institutionbanjico', verbosity=0)
        call_command('loaddata', 'statusRegistro', verbosity=0)
        Telefono.objects.create(
            telefono="5513125668",
            activo=True,
            validado=True
        )

        self._client = Client()
        self.user = get_user_model().objects.get(username='test')
        self._pass = "12345678"
        request = HttpRequest()
        authenticate(request,
            username=self.user,
            password=self._pass)
        self.token = get_token(self.user)
        print('authenticating')
        print(schema.__dict__)


class UserTests(DemograficosTestBase):

    def test_create_user(self):
        mutation = '''
        mutation CreateUser($username: String!, $password: String!) {
                createUser(
                    username: $username,
                    password: $password
                    test: true
                ){
                    user{
                        username
                    }
                 }
        }
        '''
        variables = {
            'username': '5513125668',
            'password': '123456',
        }
        res = self.client.execute(mutation, variables)
        expected_res = {
            'createUser': {
                'user': {
                    'username': '5513125668',
                }
            }
        }
        self.assertEqual(res.data, expected_res)
        print("    [assert OK] first user created")

    def test_user_profile(self):
        query = '''
        query userProfile($token: String!){
            userProfile(token: $token) {
                user{
                    firstName
                }
            }
        }
        '''
        variables = {'token': self.token}

        expected_res = {
            'userProfile':
                {
                    'user': {
                            'firstName': 'Lucia Fernanda',
                        }
                }
            }
        res = self.client.execute(query, variables)
        self.assertEqual(res.data, expected_res)
        print("    [assert OK] query user profile")

    def test_create_contacto(self):
        mutation = '''
        mutation createContacto(
                        $token: String!,
                        $nombre: String!,
                        $nombreCompleto: String!,
                        $banco: String!,
                        $clabe: String!
                      ){
                        createContacto(
                          token: $token,
                          nombre: $nombre,
                          nombreCompleto: $nombreCompleto,
                          banco: $banco,
                          clabe: $clabe
                        ){
                        allContactos{
                            clabe
                        }
                        }
                      }
                      '''
        variables = {'token': self.token,
                     'nombre': 'nombretest',
                     'nombreCompleto': 'nombreCompletotest',
                     'banco': 'bancotest',
                     'clabe': '014456789098765432'}
        res = self.client.execute(mutation, variables)
        expected_res = {
            'createContacto': {
                'allContactos': [
                    {
                        'clabe': '014456789098765432',
                    }
                ]
            }
        }
        self.assertEqual(res.data, expected_res)
        print("    [assert OK] user contact created")
