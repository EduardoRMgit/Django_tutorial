# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from .testdb import load_min_test
from django.core.management import call_command


class JWTAuthClientTestCase(JSONWebTokenTestCase):
    """ Clase modelo con la instancia de un usuario existente y
        un cliente autenticado. Con fixtures incluidos. """

    def setUp(self):
        load_min_test()
        call_command('loaddata', 'nivelCuenta', verbosity=0)
        call_command('loaddata', 'entidad_federativa', verbosity=0)
        call_command('loaddata', 'tipoDireccion', verbosity=0)
        call_command('loaddata', 'direccion', verbosity=0)
        call_command('loaddata', 'urls', verbosity=0)
        call_command('loaddata', 'contable_cuenta', verbosity=0)
        call_command('loaddata', 'tipo_contable_cuenta', verbosity=0)
        call_command('loaddata', 'cuenta_saldo', verbosity=0)
        call_command('loaddata', 'contactos', verbosity=0)

        self.user = get_user_model().objects.get(username='test')
        self.client.authenticate(self.user)
