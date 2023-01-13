# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.core.management import call_command

from graphql_jwt.shortcuts import get_token

from ..auth_client import JWTAuthClientTestCase
from demograficos.models import Telefono


class TokenTests(JWTAuthClientTestCase):
    """ Pruebas de la mutación tokenAuth. """

    def setUp(self):
        call_command('loaddata', 'nivelCuenta', verbosity=0)

    def test_client_token_integrity(self):
        """ Prueba que el token que el cliente envía en los headers
            conicide con el del usuario. """

        client_token = self.client._credentials['HTTP_AUTHORIZATION'][4:]
        user_token = get_token(self.user)
        self.assertEqual(client_token, user_token)

    def test_token_auth(self):
        """ Prueba que el token recibido con la mutación, conicide
            con el del usuario. Y por transitividad, prueba que el token
            que se envía en los headers conincide con el que se recibe
            con la mutación. """

        mutation = '''
        mutation getToken($username: String!, $password: String!) {
            tokenAuth(username: $username, password: $password)
            {
                token
            }
        }
        '''

        # Credenciales válidas
        variables = {
            'username': 'test',
            'password': '12345678',
        }
        res = self.client.execute(mutation, variables)
        self.assertEqual(res.data['tokenAuth']['token'],
                         get_token(self.user))

        # Credenciales incorrectas
        variables = {
            'username': 'test',
            'password': '00000000',
        }
        res = self.client.execute(mutation, variables)
        self.assertEqual(res.data['tokenAuth'], None)
        self.assertEqual(res.errors[0].message,
                         'Usuario y/o contraseña incorrectos')


class CreateUserTests(JWTAuthClientTestCase):
    """ Pruebas de la mutación createUser. """

    def setUp(self):
        call_command('loaddata', 'statusRegistro', verbosity=0)
        Telefono.objects.create(
            telefono="5551029634",
            activo=True,
            validado=True
        )

    def test_create_user(self):
        """ Prueba la mutación createUser.
            Creación de un nuevo usuario su autenticacion. """

        # Creación de un usuario nuevo
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
            'username': '5551029634',
            'password': 'Qwerty123456',
        }

        res = self.client.execute(mutation, variables)

        # Verificamos su creación recuperándolo de la base de datos.
        new_user = get_user_model().objects.get(username='5551029634')
        self.assertEqual(res.data['createUser']['user']['username'],
                         new_user.username)

        # Verificamos la autenticación del nuevo usuario, obteniendo su perfil.
        self.client.authenticate(new_user)
        query = '''
             query GetUserProfile {
               userProfile {
                 user {
                   username
                 }
               }
             }
        '''
        variables = {}
        res = self.client.execute(query, variables)
        self.assertEqual(res.data['userProfile']['user']['username'],
                         new_user.username)


class UserProfileTests(JWTAuthClientTestCase):
    """ Prueba la query userProfile. """

    def test_user_profile(self):
        """ Prueba únicamente la mutación userProfile (requiere autenticación).
            Usamos el usuario asociado al cliente, instanciado en la
            clase padre JWTAuthClientTestCase. """

        self.client.authenticate(self.user)
        query = '''
             query GetUserProfile {
               userProfile {
                 user {
                   username
                 }
               }
             }
        '''
        variables = {}
        res = self.client.execute(query, variables)
        self.assertEqual(res.data['userProfile']['user']['username'],
                         self.user.username)
