
from ..auth_client import JWTAuthClientTestCase

import json

from collections import OrderedDict

from django.core.management import call_command


class GetUserProfileTest(JWTAuthClientTestCase):

    def test_get_user_profile(self):
        call_command('loaddata', 'statusCuenta', verbosity=0)
        call_command('loaddata', 'nivelCuenta', verbosity=0)
        call_command('loaddata', 'docAdjuntoTipo', verbosity=0)
        call_command('loaddata', 'docAdjunto', verbosity=0)
        call_command('loaddata', 'indiceDisponible', verbosity=0)
        call_command('loaddata', 'userProfile', verbosity=0)

        query = '''
             query UP{
                userProfile{
                    sexo
                    fechaNacimiento
                    nacionalidad
                    apMaterno
                    ocupacion
                    numeroIne
                    curp
                    rfc
                    ciudadNacimiento
                    user{
                        firstName
                        lastName
                    }
                }
            }
        '''
        variables = {}
        res = self.client.execute(query, variables)
        string = '''
            {
              "data": {
                "userProfile": {
                  "sexo": "F",
                  "fechaNacimiento": null,
                  "nacionalidad": "",
                  "apMaterno": "Contreras",
                  "ocupacion": "",
                  "numeroIne": null,
                  "curp": "AAZD911216YVM05",
                  "rfc": null,
                  "ciudadNacimiento": "",
                  "user": {
                    "firstName": "Lucia Fernanda",
                    "lastName": "Brativano"
                  }
                }
              }
            }
        '''
        my_dict = json.loads(string, object_pairs_hook=OrderedDict)
        print(res.data)
        print(my_dict)
        self.assertEqual(res.data, my_dict['data'])
