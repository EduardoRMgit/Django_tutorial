from graphql_jwt.testcases import JSONWebTokenTestCase
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import get_user_model
from django.core.management import call_command
import json


class TestBeneficiario(JSONWebTokenTestCase):

    def setUp(self):
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
                                    $name:String!,
                                    $parentesco:Int!){
                createBeneficiario(
                  token: $token,
                  name: $name,
                  parentesco: $parentesco,
                ){
                  beneficiario{
                    nombre
                    id
                  }
                }
              }
              '''
        variables = {
                    "token": self.token,
                    "name": "Aurora",
                    "parentesco": 3}
        expected_res = {
                  "nombre": "Aurora",
                  "id": "1",
        }

        res = self.client.execute(mutation, variables)
        my_dict = res.data['createBeneficiario']['beneficiario']
        my_dict_ = json.dumps(my_dict)
        expected_res_ = json.dumps(expected_res)
        self.assertEqual(my_dict_, expected_res_)
        # variables["linea1"] = variables["linea1"]+"1"
        # res = self.client.execute(mutation, variables)
        # self.assertNotEqual(res.data, expected_res)
