from graphql_jwt.testcases import JSONWebTokenTestCase
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import get_user_model
from django.core.management import call_command
from demograficos.models import Avatar
from django.core.files.images import ImageFile


class TestInfopersonal(JSONWebTokenTestCase):

    def setUp(self):
        call_command('loaddata', 'component', verbosity=0)
        call_command('loaddata', 'adminUtils', verbosity=0)
        call_command('loaddata', 'nivelCuenta', verbosity=0)
        call_command('loaddata', 'usertesting', verbosity=0)
        call_command('loaddata', 'statusRegistro', verbosity=0)
        call_command('loaddata', 'entidad_federativa', verbosity=0)
        Avatar.objects.create(
            avatar_img=ImageFile(open("Zygoovertical-01.jpg", "rb")),
            name="test",
            description="test"
        )

        self.user = get_user_model().objects.get(username='test')

        self.token = get_token(self.user)

    def test_updateInfoPersonal(self):

        # No hay validación en RENAPO entonces establecemos CURP
        self.user.Uprofile.curp = "VAQD970909HASLJN03"
        self.user.Uprofile.save()

        mutation = '''
        mutation UpdateInfoPersonal($token:String!,
                                    $name:String!,
                                    $lastName_P:String!,
                                    $lastName_M:String!,
                                    # $birthDate:Date,
                                    $gender:String!,
                                    $nationality:String!,
                                    $city:String!,
                                    $occupation:String!,
                                    # $curp:String!,
                                    $rfc:String){
                updateInfoPersonal(
                            token: $token,
                            name: $name,
                            lastNameP: $lastName_P,
                            lastNameM: $lastName_M,
                            # birthDate: $birthDate,
                            gender: $gender,
                            nationality: $nationality,
                            city: $city,
                            occupation: $occupation,
                            # curp: $curp,
                            rfc: $rfc){
                    user{
                        firstName
                        lastName
                        Uprofile{
                          alias
                          apMaterno
                          sexo
                          nacionalidad
                          ciudadNacimiento
                          ocupacion
                          # curp
                          # rfc
                          # fechaNacimiento
                        }
                    }
                }
        }
        '''
        variables = {"token": self.token,
                     "name": "TestName",
                     "lastName_P": "ApellidoPTest",
                     "lastName_M": "ApellidoMTest",
                     "gender": "trans",
                     "nationality": "Mexicano",
                     "city": "2",
                     "occupation": "tester",
                     # "rfc": "VAQD970909H96",
                     # "curp": "VAQD970909HASLJN03",
                     # "birthDate": "1999-08-13"
                     }
        res = self.client.execute(mutation, variables)
        expected_res = {
            "updateInfoPersonal": {
                "user": {
                    "firstName": "TestName",
                    "lastName": "ApellidoPTest",
                    "Uprofile": {
                        "alias": "TestName17",
                        "apMaterno": "ApellidoMTest",
                        "sexo": "trans",
                        "nacionalidad": "Mexicano",
                        "ciudadNacimiento": "2",
                        "ocupacion": "tester",
                        # "curp": "VAQD970909HASLJN03",
                        # "rfc": "VAQD970909H96",
                        # "fechaNacimiento": "1999-08-13",
                    }
                }
            }
        }
        self.assertEqual(res.data, expected_res)
        print("  Info Personal ... Ejecutando")
