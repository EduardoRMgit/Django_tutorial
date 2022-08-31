from graphql_jwt.testcases import JSONWebTokenTestCase
from django.core.management import call_command
from django.test import Client


class AllCountriesTest(JSONWebTokenTestCase):

    def setUp(self):
        call_command('loaddata', 'countries', verbosity=0)
        self._client = Client()

    def test_all_countries(self):

        query = '''
                query allCountries{
                    allCountries{
                        id
                        country
                    }
                }
        '''
        variables = {}
        res = self.client.execute(query, variables)
        self.assertEqual(res.data['allCountries'][112]['country'],
                         "PN:Islas Pitcairn")
