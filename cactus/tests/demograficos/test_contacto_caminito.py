from graphql_jwt.testcases import JSONWebTokenTestCase
from django.test import Client
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import get_user_model
from django.core.management import call_command
import string
import random
from django.contrib.auth import authenticate
from django.http import HttpRequest


class TestContacto(JSONWebTokenTestCase):
    """
    Pruebas a creación y actualizacion de contacto del usuario.
    ---------------------------------------
        Se prueba en cuatro pasos la creación y actualización del contacto de
        un usuario.
        Dentro del test también se inducen los posibles errores para confirmar
        la respuesta negativa dentro del enrolamiento.
    """
    """
    1 Mutación: createContacto
            <Con token incorrecto>
            - Inducimos el error con un token incorrecto (generado de forma
              aleatoria) comparando que la respuesta de la mutación y la
              respuesta del error esperado sean la misma.
            <Con token correcto>
            - Para la creación del contacto se genera un token único para el
              usuario y se introducen los datos del contacto (nombre, banco,
              clabe, etc.). El token generado debe ser válido para la creación
              del contacto. Comparamos la respuesta de la mutación
              con la respuesta esperada.
    2 Mutación: updateContacto
            <Con id incorrecto>
            - Inducimos el error con un id de contacto incorrecto, comparando
              que la respuesta de la mutación y la respuesta del error esperado
              sean la misma.
            <Con token incorrecto>
            - Inducimos el error con un token incorrecto (generado de forma
              aleatoria) comparando que la respuesta de la mutación y la
              respuesta del error esperado sean la misma.
            <Con token, id correctos>
            - Para la actualización del contacto se genera un token único para
              el usuario y se cambian los datos del contacto del mismo. El
              token debe ser válido para generar los cambios. Comparamos la
              respuesta de la mutación con la respuesta esperada.
    3 Mutación: deleteContacto
            <Con clabe incorrecta>
            - Inducimos el error con una clabe incorrecta, comparando
              que la respuesta de la mutación y la respuesta del error esperado
              sean la misma.
            <Con token incorrecto>
            - Inducimos el error con un token incorrecto (generado de forma
              aleatoria) comparando que la respuesta de la mutación y la
              respuesta del error esperado sean la misma.
            <Con token, clabe correctos>
            - Para desactivar el contacto se genera el token único del usuario
              y se introducen los datos correctos necesarios del contacto.
              El token debe ser válido para generar los cambios. Comparamos la
              respuesta de la mutación con la respuesta esperada.
    4 Query: allContactos
            <Con token incorrecto>
            - Inducimos el error con un token incorrecto (generado de forma
              aleatoria) comparando que la respuesta de la mutación y la
              respuesta del error esperado sean la misma.
            <Con token correcto>
            - Constatamos que el contacto eliminado, con su respectivo token de
              usuario, se encuentre en la base de datos como inactivo.
        """
    @classmethod
    def setUpTestData(self):
        call_command('loaddata', 'nivelCuenta', verbosity=0)
        call_command('loaddata', 'usertesting', verbosity=0)
        call_command('loaddata', 'institutionbanjico', verbosity=0)

        self._client = Client()
        self.user = get_user_model().objects.get(username='test')
        self._pass = "12345678"
        request = HttpRequest()
        authenticate(request,
            username=self.user,
            password=self._pass)
        self.token = get_token(self.user)

    def test_contacto(self):
        # (createContacto)' <con token incorrecto>
        letters_and_digits = string.ascii_letters + string.digits
        token_wrong = ''.join(
            (random.choice(letters_and_digits) for i in range(158)))
        mutation = '''
            mutation createContacto(
                            $token: String!,
                            $nombre: String!,
                            $nombreCompleto: String!,
                            $banco: String!,
                            $clabe: String!,
                            $nip: String!
                        ){
                            createContacto(
                            token: $token,
                            nombre: $nombre,
                            nombreCompleto: $nombreCompleto,
                            banco: $banco,
                            clabe: $clabe,
                            nip: $nip
                            ){
                            allContactos{
                                clabe
                            }
                            }
                        }
            '''
        variables = {'token': str(token_wrong),
                     'nombre': 'miaumiau',
                     'nombreCompleto': 'wazap',
                     'banco': 'fake',
                     'clabe': '014122223333444455',
                     'nip': '1234'}
        res = self.client.execute(mutation, variables)
        self.assertEqual(res.errors[0].message,
                         'Error decoding signature')
        print("    [assert OK] Wrong token for createContacto   ")

    # createContacto con variables correctas
        variables2 = {'token': self.token,
                     'nombre': 'miaumiau',
                     'nombreCompleto': 'wazap',
                     'banco': 'fake',
                     'clabe': '014122223333444455',
                     'nip': '1234'}
        self.user.Uprofile.set_password("1234")
        self.user.Uprofile.save()
        res2 = self.client.execute(mutation, variables2)
        expected_res = {
                "createContacto": {
                     "allContactos": [
                        {
                            "clabe": "014122223333444455",
                        }
                      ]
                 }
             }
        self.assertEqual(res2.data, expected_res)
        print("    [assert OK] User contact, created")

    # def test_update_contacto(self):
        mutation2 = '''
            mutation updateContacto($token: String!,
                                    $id: Int!,
                                    $nombre: String!,
                                    $apPaterno: String!,
                                    $apMaterno: String!){
                updateContacto(token: $token,
                                id: $id,
                                nombre: $nombre,
                                apPaterno: $apPaterno,
                                apMaterno: $apMaterno){
                    contacto{
                    id
                    nombre
                    apPaterno
                    apMaterno
                    }
                }
            }
        '''
        # Probamos <con id incorrecto>
        variables3 = {"token": self.token,
                      "id": 2,
                      "nombre": "Rufina",
                      "apPaterno": "Rufistofilus",
                      "apMaterno": "Maxima"}
        res3 = self.client.execute(mutation2, variables3)
        self.assertEqual(res3.errors[0].message,
                         'Contacto matching query does not exist.')
        print("    [assert OK] Wrong ID for updateContacto")

        # Ahora el (test)' de updateContacto <con token incorrecto>
        letters_and_digits = string.ascii_letters + string.digits
        token_wrong2 = ''.join(
            (random.choice(letters_and_digits) for i in range(158)))
        variables4 = {"token": str(token_wrong2),
                      "id": 2,
                      "nombre": "Rufina",
                      "apPaterno": "Rufistofilus",
                      "apMaterno": "Maxima"}
        res4 = self.client.execute(mutation2, variables4)
        self.assertEqual(res4.errors[0].message,
                         'Error decoding signature')
        print("    [assert OK] Wrong Token for updateContacto")

        # updateContacto con variables correctas
        variables5 = {"token": self.token,
                      "id": 1,
                      "nombre": "Antonio",
                      "apPaterno": "Robles",
                      "apMaterno": "Torres"}
        res5 = self.client.execute(mutation2, variables5)
        expected_res = {
                 "updateContacto": {
                    "contacto": {
                        "id": "1",
                        "nombre": "Antonio",
                        "apPaterno": "Robles",
                        "apMaterno": "Torres"
                        }
                    }
                }
        self.assertEqual(res5.data, expected_res)
        print("   [assert OK] updateContacto, done    ")

    # def test_delete_contacto(self):
        mutation3 = '''
                mutation deleteContacto($token: String!,
                                        $clabe: String!,
                                        $tokenD: String!){
                    deleteContacto(token: $token,
                                   clabe: $clabe,
                                   tokenD: $tokenD){
                        contacto{
                                nombre
                                activo
                        }
                    }
                }
        '''
        mutation30 = '''
                query tokenDinamico($token: String!){
                    tokenDinamico(token: $token){
                        token
                    }
                }
        '''
        variable60 = {"token": self.token}
        res60 = self.client.execute(mutation30, variable60)
        # (deleteContacto)' <con clabe incorrecta>
        variables6 = {"token": self.token,
                      "clabe": "014111111111111111",
                      "tokenD": res60.data["tokenDinamico"]["token"]}
        res6 = self.client.execute(mutation3, variables6)
        self.assertEqual(res6.errors[0].message,
                         'No existe contacto activo')
        print("    [assert OK] Wrong CLABE for deleteContacto")

        # Ahora el (test)' deleteContacto <con token incorrecto>
        letters_and_digits = string.ascii_letters + string.digits
        token_wrong3 = ''.join(
            (random.choice(letters_and_digits) for i in range(158)))
        variables7 = {"token": str(token_wrong3),
                      "clabe": "014122223333444455",
                      "tokenD": res60.data["tokenDinamico"]["token"]}
        res7 = self.client.execute(mutation3, variables7)
        self.assertEqual(res7.errors[0].message,
                         'Error decoding signature')
        print("    [assert OK] Wrong token for deleteContacto")

        # deleteContacto con variables correctas
        res60 = self.client.execute(mutation30, variable60)
        variables8 = {"token": self.token,
                      "clabe": "014122223333444455",
                      "tokenD": res60.data["tokenDinamico"]["token"]}
        res8 = self.client.execute(mutation3, variables8)
        expected_res = {
                    "deleteContacto": {
                        "contacto": {
                            "nombre": "Antonio",
                            "activo": False
                        }
                    }
                }
        self.assertEqual(res8.data, expected_res)
        print("    [assert OK] deleteContacto, done")

        # Revisar en query que este inactivo
        query = '''
            query allContactos($token: String!){
                allContactos(token: $token){
                    activo
                }
            }
        '''
        # (query test)' de userProfile <con token incorrecto>
        letters_and_digits = string.ascii_letters + string.digits
        token_wrong4 = ''.join(
            (random.choice(letters_and_digits) for i in range(158)))

        variables = {"token": str(token_wrong4)}
        res = self.client.execute(query, variables)
        self.assertEqual(res.errors[0].message,
                         'Error decoding signature')
        print("    [assert OK] Wrong Token for query allContactos  ")

        # Query allContactos con variables correctas
        variables = {'token': self.token}
        res = self.client.execute(query, variables)
        self.assertEqual(res.data['allContactos'][0]['activo'], False)
        print("    [assert OK] Contacts in order!  ")
