# -*- coding: utf-8 -*-
"""
These tests have the purpose of verifying the correct functioning of
Transaction APP
"""

from ..common import CactusGraphQLTestCase
from ..testdb import load_min_test
from django.core.management import call_command


class TestTransactionGraphQL(CactusGraphQLTestCase):

    def setUp(self):
        call_command('loaddata', 'nivelCuenta', verbosity=0)
        load_min_test()
        super().setUp()

    def test_transaction_query(self):

        query = """
        query {
            allTransaccion{
                id
                fechaTrans
                fechaVencimiento
                monto
                comision
            }
        }
        """
        expected_res = {
            'allTransaccion':
            [
                {
                    'id': '1',
                    'fechaTrans': '2019-08-01T22:50:33+00:00',
                    'fechaVencimiento': '2019-08-01T22:50:33+00:00',
                    'monto': 34568.0,
                    'comision': 3456.0},
                {
                    'id': '2',
                    'fechaTrans': '2019-08-01T22:53:51+00:00',
                    'fechaVencimiento': '2019-08-01T22:53:51+00:00',
                    'monto': 346.0,
                    'comision': 34.0
                }
            ]
        }
        response = self.query(query)
        self.assertResponseNoErrors(response, expected_res)
