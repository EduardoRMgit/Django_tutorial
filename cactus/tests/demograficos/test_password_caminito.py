from graphql_jwt.testcases import JSONWebTokenTestCase
from django.test import Client
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import get_user_model
from django.core.management import call_command
import string
import random
from django.contrib.auth import authenticate
from django.http import HttpRequest


class PasswordTestBase(JSONWebTokenTestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'adminUtils', verbosity=0)
        call_command('loaddata', 'statusRegistro', verbosity=0)
        call_command('loaddata', 'component', verbosity=0)
        call_command('loaddata', 'preguntas_secretas', verbosity=0)
        call_command('loaddata', 'usertesting', verbosity=0)

    def setUp(self):
        self._client = Client()
        self.user = get_user_model().objects.get(username='test')
        self._pass = "12345678"
        request = HttpRequest()
        authenticate(request,
            username=self.user,
            password=self._pass)
        self.token = get_token(self.user)


class TestPreguntaNipPassword(PasswordTestBase):

    # Caminito (createUpdatePregunta + tokenAuthPreguntaNip) y sus negaciones
    # por si se olvida de la pregunta y/o quisiera recuperar el nip
    def test_create_update_pregunta(self):
        """
        Se prueba en dos pasos la creacion/actualizacion de la pregunta de
        seguridad para recuperar el nip del usuario.
        Dentro del test también se inducen los posibles errores para confirmar
        la respuesta negativa dentro del enrolamiento.
        """
        """
        1 Mutación: createUpdatePregunta
            <Con token incorrecto>
            - Inducimos el error con un token incorrecto (generado de forma
            aleatoria) comparando que la respuesta negativa de la mutación y la
            respuesta del error esperado sean la misma.
            <Con token correcto>
            - Para establecer y modificar la pregunta y respuesta secreta del
            usuario se requiere un token único del mismo. El token debe ser
            válido para generar los cambios. Comparamos la respuesta de la
            mutación con la respuesta esperada.
        2 Mutación: tokenAuthPreguntaNip
            <Con variables correctas>
            - Con la autenticacion de la pregunta y respuestaSecreta
            actualizados en la primera mutación, recupremamos el nip del
            usuario.
        """
        mutation = """
        mutation createUpdatePregunta($preguntaId: Int!,
                                      $respuesta: String!,
                                      $token: String!){
                createUpdatePregunta(preguntaId: $preguntaId,
                                     respuesta: $respuesta,
                                     token: $token){
                    pregunta{
                        id
                        pregunta
                    }
                    respuesta{
                        respuestaSecreta
                        user{
                            username
                        }
                    }
                }
            }
        """
        # (test)' createUpdatePregunta <con token incorrecto>
        letters_and_digits = string.ascii_letters + string.digits
        token_wrong = ''.join(
            (random.choice(letters_and_digits) for i in range(158)))

        variables = {'token': str(token_wrong),
                     'preguntaId': 1,
                     'respuesta': "Futbol"}
        res = self.client.execute(mutation, variables)
        self.assertEqual(res.errors[0].message,
                         'Error decoding signature')
        print("    [assert OK] Wrong token for createUpdatePregunta")

        # createUpdatePregunta <con token correcto>
        variables = {'token': self.token,
                     'preguntaId': 1,
                     'respuesta': "Futbol"}
        expected_res = {
            "createUpdatePregunta": {
                "pregunta": {
                    "id": "1",
                    "pregunta": "¿Cuál es tu deporte favorito?"
                },
                "respuesta": {
                    "respuestaSecreta": "Futbol",
                    "user": {
                        "username": "test"
                     }
                }
            }
        }
        res = self.client.execute(mutation, variables)
        self.assertEqual(res.data, expected_res)
        print("    [assert OK] Se asigno pregunta de seguridad a usuario test")

        # Test tokenAuthPreguntaNip
        mutation2 = """
        mutation tokenAuthPreguntaNip($preguntaId: Int!,
                                      $respuestaSecreta: String!,
                                      $username: String!){
                tokenAuthPreguntaNip(preguntaId: $preguntaId,
                                     respuestaSecreta: $respuestaSecreta,
                                     username: $username){
                    token
                    nip
                }
            }
        """
        variables2 = {'preguntaId': 1,
                      'respuestaSecreta': "Futbol",
                      'username': "test"}
        res2 = self.client.execute(mutation2, variables2)
        expected_res2 = {
            "tokenAuthPreguntaNip": {
                "token": res2.data['tokenAuthPreguntaNip']['token'],
                "nip": res2.data['tokenAuthPreguntaNip']['nip']
            }
        }
        self.assertEqual(res2.data, expected_res2)

    # Caminito (generateNipTemp + updateNip) y sus negaciones
    # por si se quisiera cambiar el nip
    def test_generate_nip_temp(self):
        """
        Se prueba en dos pasos la actualizacion de Nip del usuario. En la
        primera mutación se genera un NipTemporal para después autentificarse y
        actualizar Nip de forma segura.
        Dentro del test también se inducen los posibles errores para confirmar
        la respuesta negativa dentro del enrolamiento.
        """
        """
        1 Mutación: generateNipTemp
            <Con token incorrecto>
            - Inducimos el error con un token incorrecto (generado de forma
            aleatoria) comparando que la respuesta negativa de la mutación y la
            respuesta del error esperado sean la misma.
            <Con token correcto>
            - Para generar el NipTemporal del usuario se requiere un token únic
            del mismo. El token debe ser válido para generar el NipTemporal.
            Comparamos la respuesta de la mutación con la respuesta esperada.
        2 Mutación: updateNip
            <Con token incorrecto>
            - Inducimos el error con un token incorrecto (generado de forma
            aleatoria) comparando que la respuesta negativa de la mutación y la
            respuesta del error esperado sean la misma.
            <Con variables correctas>
            - Para actualizar el Nip del usuario se requiere un token único del
            mismo y el NipTemporal (generado en la primera mutación) donde
            ambos deben ser válidos para generar los cambios. Comparamos la
            respuesta de la mutación con la respuesta esperada.
        """
        mutation = '''
            mutation generateNipTemp($token: String!){
                    generateNipTemp(token: $token){
                        nipTemp
                    }
                }
            '''
        # (test)' generateNipTemp <con token incorrecto>
        letters_and_digits = string.ascii_letters + string.digits
        token_wrong2 = ''.join(
            (random.choice(letters_and_digits) for i in range(158)))

        variables = {'token': str(token_wrong2)}
        res = self.client.execute(mutation, variables)
        self.assertEqual(res.errors[0].message,
                         'Error decoding signature')
        print("    [assert OK] Wrong token for generateNipTemp")

        # generateNipTemp <con token correcto>
        variables = {"token": self.token}
        res = self.client.execute(mutation, variables)
        expected_res = {
            "generateNipTemp": {
                "nipTemp": res.data['generateNipTemp']['nipTemp']
                    }
                }
        self.assertEqual(res.data, expected_res)
        print("   [assert OK] NipTemp, created")

        nip_temp = res.data['generateNipTemp']['nipTemp']

        # test updateNip
        mutation2 = '''
            mutation updateNip($token: String!,
                               $oldNip: String!,
                               $newNip: String!){
                updateNip(token: $token
                          oldNip: $oldNip,
                          newNip: $newNip){
                    userProfile{
                    apMaterno
                    }
                }
            }
        '''
        # (test)' UpdateNip <con token incorrecto>
        letters_and_digits = string.ascii_letters + string.digits
        token_wrong3 = ''.join(
            (random.choice(letters_and_digits) for i in range(158)))

        variables = {'token': str(token_wrong3)}
        res = self.client.execute(mutation, variables)
        self.assertEqual(res.errors[0].message,
                         'Error decoding signature')
        print("    [assert OK] Wrong token for updateNip")

        # UpdateNip <con token correcto>
        variables2 = {"token": self.token,
                      "oldNip": nip_temp,
                      "newNip": "111111"}
        res2 = self.client.execute(mutation2, variables2)
        expected_res2 = {
                "updateNip": {
                    "userProfile": {
                        "apMaterno": res2.data['updateNip']['userProfile']
                                              ['apMaterno']
                    }
                }
            }
        self.assertEqual(res2.data, expected_res2)
        print("   [assert OK] UpdateNip, done")

    # Caminit createUpdatePreguntaForUser + tokenAuthPregunta + recoverPassword
    # para en caso de que se haya olvidado la password y para cambiar password
    def test_create_update_pregunta_for_user(self):
        """
        Se prueba en cuatro pasos la actualizacion de Password del usuario.
        En la primera mutación se actualiza la PreguntaForUser con Password
        para después autentificarse con su respuesta secreta y de forma segura
        actualizar Password.
        Dentro del test también se inducen los posibles errores para confirmar
        la respuesta negativa dentro del enrolamiento.
        """
        """
        1 Mutación: createUpdatePreguntaForUser
            <Con variables correctas>
            - Para establecer y modificar la pregunta y respuesta secreta del
            usuario se requiere un token único del mismo. El token debe ser
            válido para generar los cambios. Comparamos la respuesta de la
            mutación con la respuesta esperada.
        2 Mutación: tokenAuthPregunta
            - Con la respuesta a la preguntaSecreta y respuestaSecreta
            actualizados en la primera mutación, recupremamos el token y nip
            del usuario.
            Comparamos la respuesta de la mutación con la respuesta esperada.
        3 Mutación: recoverPassword
            - Para la recuperación de Password usamos el token y Nip para
            autentificar de forma segura y generar los cambios.
            Comparamos la respuesta de la mutación con la respuesta esperada.
        4 Mutación: changePassword
            - Para modificar Password de usuario se requiere un token único del
            mismo y el Password anterior. El token y el Passsword deben ser
            válidos para generar los cambios.
            Comparamos la respuesta de la mutación con la respuesta esperada.
        """
        # createUpdatePregunta
        mutation = """
        mutation createUpdatePreguntaForUser($password: String!,
                                             $username: String!,
                                             $preguntaId: Int!,
                                             $respuesta: String!){
                createUpdatePreguntaForUser(password: $password,
                                            username: $username,
                                            preguntaId: $preguntaId,
                                            respuesta: $respuesta){
                    respuesta{
                        tipoNip
                        respuestaSecreta
                        user{
                            username
                        }
                    }
                    pregunta{
                        id
                        tipoNip
                        pregunta
                    }
                }
            }
        """
        variables = {'password': '12345678',
                     'username': 'test',
                     'preguntaId': 8,
                     'respuesta': 'iron maiden'}
        expected_res = {
             "createUpdatePreguntaForUser": {
                "respuesta": {
                    "tipoNip": False,
                    "respuestaSecreta": "iron maiden",
                    "user": {
                        "username": "test"
                    }
                },
                "pregunta": {
                    "id": "8",
                    "tipoNip": False,
                    "pregunta": "¿Cuál es tu animal favorito?"
                }
             }
        }
        res = self.client.execute(mutation, variables)
        print('/////////////////////////////')
        print(res)
        self.assertEqual(res.data, expected_res)
        print(" [assert OK] Se asigno pregunta de seguridad a usuario test")

        # tokenAuthPregunta
        mutation2 = """
        mutation tokenAuthPregunta($username: String!,
                                   $preguntaId: Int!,
                                   $respuestaSecreta: String!){
                tokenAuthPregunta(username: $username,
                                  preguntaId: $preguntaId,
                                  respuestaSecreta: $respuestaSecreta){
                    token
                    pin
                }
            }
        """
        variables2 = {'preguntaId': 8,
                      'respuestaSecreta': "iron maiden",
                      'username': "test"}
        res2 = self.client.execute(mutation2, variables2)
        expected_res2 = {
            "tokenAuthPregunta": {
                "token": res2.data['tokenAuthPregunta']['token'],
                "pin": res2.data['tokenAuthPregunta']['pin']
            }
        }
        self.assertEqual(res2.data, expected_res2)
        print(" [assert OK] Pin + token a usuario test")

        new_token = res2.data['tokenAuthPregunta']['token']
        new_pin = res2.data['tokenAuthPregunta']['pin']

        # recoverPassword
        mutation3 = '''
            mutation recoverPassword($token: String!,
                                     $pin: String!,
                                     $newPassword: String!){
                recoverPassword(token: $token,
                                pin: $pin,
                                newPassword: $newPassword){
                                    details
                            }
                        }
                    '''
        variables3 = {'token': new_token,
                      'pin': new_pin,
                      'newPassword': "holasholas"}
        res3 = self.client.execute(mutation3, variables3)
        expected_res3 = {
                "recoverPassword": {
                        "details": "password recuperado"
                        }
                    }
        self.assertEqual(res3.data, expected_res3)
        print(" [assert OK] Password recuperado de usuario test!  ")

        # changePassword
        mutation4 = '''
            mutation changePassword($token: String!,
                                    $oldPassword: String!,
                                    $newPassword: String!){
                changePassword(token: $token,
                               oldPassword: $oldPassword,
                               newPassword: $newPassword){
                        user{
                        username
                        }
                    }
                }
        '''
        variables4 = {'token': new_token,
                      'oldPassword': "holasholas",
                      'newPassword': "chaochao"}
        res4 = self.client.execute(mutation4, variables4)
        expected_res4 = {
                "changePassword": {
                        "user": {
                            "username": "test"
                            }
                        }
                    }
        self.assertEqual(res4.data, expected_res4)
        print("Change password, done!")
