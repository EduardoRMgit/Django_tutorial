from graphql_jwt.testcases import JSONWebTokenTestCase
from django.test import Client
from django.core.management import call_command
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import get_user_model
from collections import OrderedDict
import json
import random
import string
from django.contrib.auth import authenticate
from django.http import HttpRequest


class TestDireccion(JSONWebTokenTestCase):
    """
    Se prueba en cinco pasos la direccion del usuario y de todos sus campos así
    como también la desactivacion de la misma.
    Dentro del test también se inducen los posibles errores para confirmar
    la respuesta negativa dentro del enrolamiento.
    """
    """
    1 Mutación: setDireccion
      <Con token incorrecto>
      - Inducimos el error con un token incorrecto (generado de forma
        aleatoria) comparando que la respuesta negativa de la mutación y la
        respuesta del error esperado sean la misma.
      <Con token correcto>
      - Para establecer y modificar la dirección del usuario se requiere un
        token único del mismo. El token debe ser válido para generar los
        cambios. Comparamos la respuesta de la mutación con la respuesta
        esperada.
    2 Query: tipoDireccion
      - Constatamos que la nueva dirección de usuario creada tenga el tipo de
        dirección correcta. Comparamos la respuesta de la query con la
        respuesta esperada.
    3 Query: direccion
      <Con token incorrecto>
      - Inducimos el error con un token incorrecto (generado de forma
        aleatoria) comparando que la respuesta negativa de la mutación y la
        respuesta del error esperado sean la misma.
      <Con token correcto>
      - Con el token del usuario constatamos que los datos de la la nueva
        dirección del mismo sean los que creamos. Comparamos la respuesta de la
        query con la respuesta esperada.
    4 Mutación: deleteDireccion
      <Con token incorrecto>
      - Inducimos el error con un token incorrecto (generado de forma
        aleatoria) comparando que la respuesta negativa de la mutación y la
        respuesta del error esperado sean la misma.
      <Con token correcto>
      - Para eliminar la dirección del usuario se requiere un token único del
        mismo. El token debe ser válido para generar los cambios. Comparamos la
        respuesta de la mutación con la respuesta esperada.
    5 Query: allDireccion
      - Se sabe que la ultima dirección creada es del usuario en cuestion.
        Constatamos que este desactivada la dirección comparando que la
        respuesta de la mutación con la respuesta esperada.
    """

    def setUp(self):
        call_command('loaddata', 'nivelCuenta', verbosity=0)
        call_command('loaddata', 'entidadFed', verbosity=0)
        call_command('loaddata', 'tipoDireccion', verbosity=0)
        call_command('loaddata', 'customer', verbosity=0)
        call_command('loaddata', 'urls', verbosity=0)
        call_command('loaddata', 'usertesting', verbosity=0)
        call_command('loaddata', 'component', verbosity=0)
        call_command('loaddata', 'docAdjuntoTipo', verbosity=0)
        call_command('loaddata', 'statusRegistro', verbosity=0)

        self._client = Client()
        self.user = get_user_model().objects.get(username='test')
        self._pass = "12345678"
        request = HttpRequest()
        authenticate(request,
            username=self.user,
            password=self._pass)
        self.token = get_token(self.user)

    def test_direccion(self):
        mutation = '''
        mutation setDireccion($token:String!,$ciudad:String!,$calle:String!,
        $n_Int:String!,$n_Ext:String!,$col:String!,$cp:String!,
        $alcaldiaMunicipio:String!,$estado:Int!){
                setDireccion(
                  token: $token,
                  ciudad: $ciudad,
                  calle: $calle,
                  numInt: $n_Int,
                  numExt: $n_Ext,
                  colonia: $col,
                  codPostal: $cp,
                  alcaldiaMunicipio: $alcaldiaMunicipio,
                  estado: $estado
                ){
                  direccion{
                    calle
                    numInt
                    numExt
                    codPostal
                    ciudad
                    delegMunicipio
                    entidadFed{
                        entidad
                    }
                  }
                }
              }
              '''
        # (test)', setDireccion <con token incorrecto>
        letters_and_digits = string.ascii_letters + string.digits
        token_wrong = ''.join(
            (random.choice(letters_and_digits) for i in range(158)))
        variables = {"token": str(token_wrong),
                     "calle": "5512345678", "n_Int": "101",
                     "n_Ext": "80", "col": "San Andrés", "cp": "13670",
                     "alcaldiaMunicipio": "Tlalpan", "estado": 1,
                     "ciudad": "DF"}
        res = self.client.execute(mutation, variables)
        self.assertEqual(res.errors[0].message,
                         'Error decoding signature')
        print("    [assert OK] Bad token for set direccion")

        # setDireccion <con token correcto>
        variables = {"token": self.token,
                     "calle": "5512345678", "n_Int": "101",
                     "n_Ext": "80", "col": "San Andrés", "cp": "13670",
                     "alcaldiaMunicipio": "Tlalpan", "estado": 1,
                     "ciudad": "DF"}
        expected_res = {
                        "setDireccion": {
                          "direccion": {
                            'calle': '5512345678',
                            'numInt': '101',
                            'numExt': '80',
                            'codPostal': '13670',
                            'ciudad': 'DF',
                            'delegMunicipio': "Tlalpan",
                            'entidadFed': {
                              'entidad': 'CDMX'
                                }
                              }
                            }
                        }
        res = self.client.execute(mutation, variables)
        self.assertEqual(res.data, expected_res)
        print("    [assert OK] Set Direccion, done")
        """ probamos si falla cambiando algún dato """
        variables["calle"] = variables["calle"]+"1"
        res = self.client.execute(mutation, variables)
        self.assertNotEqual(res.data, expected_res)

        # query tipo direccion
        query = '''
                query tipoDireccion($direccionId: Int!){
                    tipoDireccion(direccionId: $direccionId){
                        id
                        tipo
                    }
                }
        '''
        variables = {'direccionId': 1}
        res = self.client.execute(query, variables)
        string1 = '''
            {
              "data": {
                "tipoDireccion": {
                    "id": "1",
                    "tipo": "Casa"
                    }
                }
            }
        '''
        my_dict = json.loads(string1, object_pairs_hook=OrderedDict)
        self.assertEqual(res.data, my_dict['data'])
        print("    [assert OK] tipoDireccion, done")

        # def test_direccion(self):
        query = '''
             query direccion($token: String!){
                 direccion(token: $token){
                     calle
                     numInt
                     numExt
                     codPostal
                     ciudad
                     delegMunicipio
                 }
                 }
         '''
        # (test)' direccion <con token incorrecto>
        letters_and_digits = string.ascii_letters + string.digits
        token_wrong2 = ''.join(
            (random.choice(letters_and_digits) for i in range(158)))
        variables = {"token": str(token_wrong2)}
        res = self.client.execute(query, variables)
        self.assertEqual(res.errors[0].message,
                         'Error decoding signature')
        print("    [assert OK] Bad token for query direccion")

        # query direccion <con token correcto>
        variables = {'token': self.token}
        res = self.client.execute(query, variables)
        string2 = '''
             {
                 "data": {
                     "direccion": [
                     {
                         "calle": "55123456781",
                         "numInt": "101",
                         "numExt": "80",
                         "codPostal": "13670",
                         "ciudad": "DF",
                         "delegMunicipio": "Tlalpan"
                     }
                     ]
                 }
                 }
         '''
        my_dict = json.loads(string2, object_pairs_hook=OrderedDict)
        print('---------------------------------')
        print(my_dict)
        print('---------------------------------')
        print(res.data)
        self.assertEqual(res.data, my_dict['data'])
        print("    [assert OK] query direccion, done")

        # delete direccion
        mutation = '''
               mutation deleteDireccion($token: String!){
                     deleteDireccion(token: $token){
                       direccion{
                           activo
                       }
                     }
                   }
               '''
        # (test)' de deleteDireccion <con token incorrecto>
        letters_and_digits = string.ascii_letters + string.digits
        token_wrong3 = ''.join(
             (random.choice(letters_and_digits) for i in range(158)))
        variables = {"token": str(token_wrong3)}
        res = self.client.execute(mutation, variables)
        self.assertEqual(res.errors[0].message,
                         'Error decoding signature')
        print("    [assert OK] Bad token for delete direccion")

        # deleteDireccion <con token correcto>
        variables = {"token": self.token}
        res = self.client.execute(mutation, variables)
        expected_res = {
                   "deleteDireccion": {
                         "direccion": {
                             "activo": False
                           }
                       }
                   }
        self.assertEqual(res.data, expected_res)
        print("   [assert OK] delete direccion, done  ")

        # Revisar en query que este inactivo
        query2 = '''
             query{
                 allDireccion{
                   activo
                 }
               }
         '''
        # Se sabe que la ultima direccion corresponde a usuario test
        variables2 = {}
        res = self.client.execute(query2, variables2)
        self.assertEqual(res.data['allDireccion'][-1]['activo'], False)
        print("   [assert OK] Direccion inactiva   ")
