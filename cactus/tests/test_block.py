from graphql_jwt.testcases import JSONWebTokenTestCase
from django.core.management import call_command
from django.contrib.auth.models import User
import datetime
from .perms import load_groups


class Login(JSONWebTokenTestCase):
    def setUp(self):
        call_command('loaddata', 'user.json', verbosity=0)
        load_groups()

        self.mutation = '''
        mutation tokenAuth($username: String!, $password: String!){
            tokenAuth(username: $username, password: $password){
                token
            }
        }'''
        self.variables = {'username': 'test', 'password': '12345'}
        self.variables1 = {'username': 'test', 'password': '12345678'}

    def test_correcto(self):
        res = self.client.execute(self.mutation, self.variables1)
        self.assertTrue(res)

    def test_intento(self):
        self.client.execute(self.mutation, self.variables)
        res1 = self.client.execute(self.mutation, self.variables1)
        self.assertTrue(res1)

    def test_bloqueo(self):
        for i in range(5):
            self.client.execute(self.mutation, self.variables)
        error = self.client.execute(self.mutation, self.variables1)
        self.assertEqual(str(error.errors),
                         "[GraphQLLocatedError('Cuenta Bloqueada')]")

    def test_desbloqueo(self):
        for x in range(5):
            self.client.execute(self.mutation, self.variables)
        error = self.client.execute(self.mutation, self.variables1)
        self.assertEqual(str(error.errors),
                         "[GraphQLLocatedError('Cuenta Bloqueada')]")
        user = User.objects.get(username="test")
        user.Uprofile.blocked_date = (
            datetime.datetime.now() - datetime.timedelta(minutes=30))
        user.Uprofile.save()
        res = self.client.execute(self.mutation, self.variables1)
        self.assertTrue(res)
