# -*- coding: utf-8 -*-

from ..auth_client import JWTAuthClientTestCase
from graphql_jwt.shortcuts import get_token
from django.core.management import call_command

from spei.models import StpTransaction


class TokenTestCase(JWTAuthClientTestCase):

    def setUp(self):
        call_command('loaddata', 'nivelCuenta', verbosity=0)
        super().setUp()

        self.token = get_token(self.user)


class TransactionTestCase(TokenTestCase):
    """ Prueba una transacción a spei. """

    mutation = """
            mutation Transaction(
                $token: String!,
                $abono: String!,
                $nip: String!,
                $concepto: String!,
                $contacto: Int!)
        {
                createTransferenciaEnviada(
                  token: $token,
                  abono: $abono,
                  concepto: $concepto,
                  nip: $nip,
                  contacto: $contacto) {
                    stpTransaccion { stpId }
                    user { id }
                }
        }
        """
    # Se agrega token dinamico

    variables = {
        'concepto':  "prueba",
        'abono': "0.01",
        'nip': "1234",
        'contacto': 1
    }

    def test_transaction_authenticated(self):
        """ Primero probamos con el cliente autenticado
            (instanciado en la clase padre)."""

        self.variables['token'] = self.token
        # Establecemos nip
        self.user.Uprofile.set_password("123456")
        # Establecemos el saldo
        self.user.Uprofile.saldo_cuenta = 0.01
        self.user.Uprofile.save()

        response = self.client.execute(self.mutation, self.variables)

        self.assertEqual(
            response.data['createTransferenciaEnviada'][
                'stpTransaccion']['stpId'],
            StpTransaction.objects.all().last().stpId
        )
        self.assertEqual(
            response.data['createTransferenciaEnviada'][
                'user']['id'],
            str(self.user.id)
        )
