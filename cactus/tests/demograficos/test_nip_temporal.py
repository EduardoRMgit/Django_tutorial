from graphql_jwt.testcases import JSONWebTokenTestCase
from demograficos.models.userProfile import NipTemporal
from django.test import Client
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.contrib.auth import authenticate
from django.http import HttpRequest


class TestNipTemporal(JSONWebTokenTestCase):

    def setUp(self):
        call_command('loaddata', 'component', verbosity=0)
        call_command('loaddata', 'nivelCuenta', verbosity=0)
        call_command('loaddata', 'usertesting', verbosity=0)

        self._client = Client()
        self.user = get_user_model().objects.get(username='test')
        self._pass = "12345678"
        request = HttpRequest()
        authenticate(request,
            username=self.user,
            password=self._pass)
        self.token = get_token(self.user)

    def test_generateNipTemp(self):
        mutation = '''
        mutation generateNipTemp($token: String!) {
        generateNipTemp(token: $token) {
          nipTemp
          }
        }
        '''
        variables = {'token': self.token}
        response = self.client.execute(mutation, variables)
        nip = NipTemporal.objects.filter(user=self.user)[0].nip_temp
        # print(response.data['generateNipTemp']['nipTemp'])
        # comparamos el nip temporal asociado al usuario con el generado
        # por la mutation
        self.assertEqual(response.data['generateNipTemp']['nipTemp'], nip)
        print("    [assert OK] nip temp coincide")
        # comprobamos que al hacer la mutacion se desactivan las otras
        # instancias de NipTemporal y que el unico nip temporal activo  es el
        # generado por la mutacion
        response = self.client.execute(mutation, variables)
        activos = NipTemporal.objects.filter(user=self.user, activo=True)
        new_nip = response.data['generateNipTemp']['nipTemp']
        self.assertTrue(len(activos) == 1)
        self.assertTrue(activos[0].nip_temp, new_nip)
        # print(response.data['generateNipTemp']['nipTemp'])
