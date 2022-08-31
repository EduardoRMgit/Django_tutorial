from django.test import Client
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.core.management import call_command
import json
from collections import OrderedDict


class BancoTestBase(JSONWebTokenTestCase):

    def setUp(self):
        call_command('loaddata', 'institutionbanjico', verbosity=0)

        self._client = Client()


class BancoTest(BancoTestBase):

    def test_banco(self):

        query = '''
            query banco($shortName: String!){
                banco(shortName: $shortName){
                    id
                    name
                    shortName
                }
            }
        '''
        variables = {'shortName': "VOLKSWAGEN"}
        res = self.client.execute(query, variables)

        string = '''
            {
            "data": {
                "banco": {
                "id": "39",
                "name": "Volkswagen Bank, S.A., Institución de Banca Múltiple",
                "shortName": "VOLKSWAGEN"
                }
            }
            }
        '''
        my_dict = json.loads(string, object_pairs_hook=OrderedDict)
        self.assertEqual(res.data, my_dict['data'])

    def test_all_bancos(self):

        query = '''
                query{
                    allBancos{
                        id
                        name
                        shortName
                    }
                }
        '''
        variables = {}
        res = self.client.execute(query, variables)
        self.assertEqual(res.data['allBancos'][32]['shortName'], "ACTINVER")
