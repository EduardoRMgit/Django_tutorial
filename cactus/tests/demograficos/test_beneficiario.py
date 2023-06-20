from graphql_jwt.testcases import JSONWebTokenTestCase
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import get_user_model
from django.core.management import call_command
import json


class TestBeneficiario(JSONWebTokenTestCase):

    def setUp(self):
        call_command('loaddata', 'nivelCuenta', verbosity=0)
        call_command('loaddata', 'parentesco', verbosity=0)
        call_command('loaddata', 'usertesting', verbosity=0)
        call_command('loaddata', 'component', verbosity=0)
        call_command('loaddata', 'statusRegistro', verbosity=0)

        self.user = get_user_model().objects.get(username='test')
        self.token = get_token(self.user)
        self.client.authenticate(self.user)

    def test_create_beneficiario(self):
        mutation = '''
        mutation createBeneficiario($token:String!,
                                    $nip: String!,
                                    $name:String!,
                                    $apellidopat:String!,
                                    $apellidomat:String,
                                    $parentesco:Int!,
                                    $calle:String!,
                                    $numeroexterior:String!,
                                    $numerointerior:String!,
                                    $codigopostal:String!,
                                    $colonia:String!,
                                    $municipio:String!,
                                    $estado: String!,
                                    $telefono: String!,
                                    $fechaNacimiento: Date!){
                createBeneficiario(
                  token: $token,
                  nip: $nip,
                  name: $name,
                  apellidomat: $apellidomat,
                  apellidopat: $apellidopat,
                  parentesco: $parentesco,
                  calle: $calle,
                  numeroexterior: $numeroexterior,
                  numerointerior: $numerointerior,
                  codigopostal: $codigopostal,
                  colonia: $colonia,
                  municipio: $municipio,
                  estado: $estado,
                  telefono: $telefono,
                  fechaNacimiento: $fechaNacimiento

                ){
                  beneficiario{
                    nombre
                    id
                  }
                }
              }
              '''
        self.user.Uprofile.set_password("1234")
        self.user.Uprofile.save()
        variables = {
                    "token": self.token,
                    "nip": "1234",
                    "name": "Aurora",
                    "apellidopat": "perez",
                    "apellidomat": "paz",
                    "parentesco": 3,
                    "calle": "avenida siempre viva",
                    "numeroexterior": "420",
                    "numerointerior": "66",
                    "codigopostal": "10910",
                    "colonia": "col",
                    "municipio": "Tlalpan",
                    "estado": "CDMX",
                    "telefono": "5578094114",
                    "fechaNacimiento": "1990-05-28"}
        expected_res = {
                  "nombre": "Aurora",
                  "id": "1",
        }

        res = self.client.execute(mutation, variables)
        my_dict = res.data['createBeneficiario']['beneficiario']
        my_dict_ = json.dumps(my_dict)
        print(my_dict_)
        expected_res_ = json.dumps(expected_res)
        print(expected_res_)
        self.assertEqual(my_dict_, expected_res_)
        # variables["linea1"] = variables["linea1"]+"1"
        # res = self.client.execute(mutation, variables)
        # self.assertNotEqual(res.data, expected_res)
