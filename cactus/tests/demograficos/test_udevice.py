from graphql_jwt.testcases import JSONWebTokenTestCase
import json
from django.core.management import call_command
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import get_user_model
from django.test import Client
from ..perms import load_groups


class TestUpdateDevice(JSONWebTokenTestCase):

    def setUp(self):

        call_command('loaddata', 'adminUtils', verbosity=0)
        load_groups()
        call_command('loaddata', 'user', verbosity=0)
        call_command('loaddata', 'proveedorTelefonico', verbosity=0)
        call_command('loaddata', 'tipoTelefono', verbosity=0)
        call_command('loaddata', 'telefono', verbosity=0)
        call_command('loaddata', 'component', verbosity=0)

        self._client = Client()
        self.user = get_user_model().objects.get(username='test')
        self._client.login(username=self.user.username)
        self.token = get_token(self.user)

    def test_register_device(self):
        from django.contrib.auth import get_user_model
        from demograficos.models import Telefono
        user = self.user
        device_id = 'uuid'
        numero = "5562059807"
        telefono = Telefono.objects.create(user=user, activo=True,
                                           telefono=numero)

        """aseguramos que despues de iniciar sesion y registrar el dipositivo,
            el usuario tiene exactamente un dispositivo udevice activo"""

        self.login_user(user, device_id)
        self.register_device(telefono, device_id)
        self.assertTrue(user.udevices.filter(activo=True).count() == 1)

        uuid = user.location.last().device.uuid

        """nos aseguramos que el uuid capturado en el middleware coincide con /
        el registrado después de la mutación"""
        self.assertTrue(user.udevices.get(activo=True).uuid == uuid)

        """creamos a otro usuario y tratamos de registrar el mismo /
        dispositivo"""

        other = get_user_model().objects.create(username='test2')
        self.login_user(other, device_id)
        other_tel = Telefono.objects.create(user=other, telefono='55555555')
        self.register_device(telefono=other_tel, device_id=device_id)
        self.assertTrue(other.udevices.count() == 0)
        self.assertTrue(
                other.componentvalidated_set.filter(status='IN').count() > 0)

        """autenticamos al usuario desde otro dispositivo y aseguramos que se /
        active la pantalla de emergencia"""

        self.login_user(user, device_id + '0')
        component = user.componentvalidated_set.get(status='IN').component
        self.assertTrue(component.alias == 'dispositivo')

    def login_user(self, user, device_id):
        user.set_password('x')
        user.save()
        auth = """mutation auth($username:String!, $password:String!){
        tokenAuth(username:$username, password:$password){
            token
            }
        }"""
        variables = {
            "username": user.username,
            "password": 'x'
        }
        data = {"query": auth, "variables": json.dumps(variables)}
        self._client.post('http://localhost:8000/graphql', json.dumps(data),
                          content_type='application/json',
                          HTTP_DEVICE_ID=device_id)

    def register_device(self, telefono, device_id):
        telefono.send_token(test=True)
        pin = telefono.PVTelefono.last().token
        register_device = """mutation ValidacionTelefono($numero:String!, $pin:String!){
        validacionTelefono(numero: $numero, pin: $pin){
            validacion
        }
        }"""
        variables = {
            "numero": telefono.telefono,
            "pin": pin,
        }
        data = {"query": register_device, "variables": json.dumps(variables)}
        self._client.post('http://localhost:8000/graphql', json.dumps(data),
                          content_type='application/json')
