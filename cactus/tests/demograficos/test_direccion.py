from graphql_jwt.testcases import JSONWebTokenTestCase
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import get_user_model
from django.core.management import call_command
from collections import OrderedDict
import json


class TestDireccion(JSONWebTokenTestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'entidad_federativa', verbosity=0)
        call_command('loaddata', 'tipoDireccion', verbosity=0)
        call_command('loaddata', 'nivelCuenta', verbosity=0)
        call_command('loaddata', 'usertesting', verbosity=0)
        call_command('loaddata', 'component', verbosity=0)
        call_command('loaddata', 'docAdjuntoTipo', verbosity=0)
        call_command('loaddata', 'statusRegistro', verbosity=0)

    def setUp(self):
        self.user = get_user_model().objects.get(username='test')
        self.token = get_token(self.user)
        self.client.authenticate(self.user)

    def test_set_direccion(self):
        mutation = '''
        mutation setDireccion($token:String!,$ciudad:String,$calle:String,
        $n_Int:String,$n_Ext:String,$col:String,$cp:String,
        $alcaldiaMunicipio:String,$estado:Int){
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
        variables = {"token": self.token,
                     "calle": "5512345678",
                     "n_Int": "101",
                     "n_Ext": "80", "col": "San Andrés", "cp": "13670",
                     "alcaldiaMunicipio": "Tlalpan", "tel": "5555555",
                     "estado": 1, "ciudad": "DF"}
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
        print("    [assert OK] set direccion mutation")
        """ probamos si falla cambiando algún dato """
        variables["calle"] = variables["calle"]+"1"
        res = self.client.execute(mutation, variables)
        self.assertNotEqual(res.data, expected_res)

    def test_get_direccion(self):
        query = '''
                 query getDireccion{
                    direccion{
                      id
                      linea1
                      linea2
                      numInt
                      numExt
                      codPostal
                      ciudad
                      delegMunicipio
                      country
                      colonia
                      telefono
                      entidadFed{
                        entidad
                      }
                    }
                  }
        '''
        # ya tiene al client logineado
        variables = {}
        res = self.client.execute(query, variables)
        string = '''
            {
              "data": {
                "direccion": [
                  {
                    "id": "5",
                    "linea1": "Madero no. 69",
                    "linea2": "Ampliacion Tepepan",
                    "numInt": null,
                    "numExt": null,
                    "codPostal": "42069",
                    "ciudad": "CDMX",
                    "delegMunicipio": "Tlalpan",
                    "country": "MX",
                    "colonia": null,
                    "telefono": null,
                    "entidadFed": {
                    "entidad": "Aguascalientes"
                    }
                  }
                ]
              }
            }
        '''
        my_dict = json.loads(string, object_pairs_hook=OrderedDict)
        self.assertEqual(res.data, my_dict['data'])
