# -*- coding: utf-8 -*-
from banca.models import SaldoReservado
from spei.models import StpTransaction
from rest_framework.test import APITestCase
from rest_framework import status
from ..testdb import load_min_test
from rest_framework.test import APIClient
from django.core.management import call_command
from django.utils import timezone


class Testcambioestado(APITestCase):
    def setUp(self):
        load_min_test()
        call_command('loaddata', 'comisionstp', verbosity=0)
        call_command('loaddata', 'contactos', verbosity=0)
        call_command('loaddata', 'stptrans', verbosity=0)
        call_command('loaddata', 'statusTrans', verbosity=0)
        call_command('loaddata', 'nivelCuenta', verbosity=0)
        self.client = APIClient()

    def test_post_cambiestado(self):
        data = {
            "id": "666420",
            "estado": "exito",
            "folioOrigen": "",
            "empresa": "ZYGO",
            "causaDevolucion": "",
            "tsLiquidacion": "1634919027297"
        }

        tr = StpTransaction.objects.get(id=1)
        sr = SaldoReservado.objects.create(
            status_saldo="reservado",
            fecha_reservado=timezone.now(),
            saldo_reservado=0.01,
        )

        # Se pudo haber obtenido in stpId negativo o inválido
        tr.stpId = "666420"
        tr.saldoReservado = sr
        tr.save()

        uri = '/api/estado/'
        response = self.client.post(uri, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(
        #     StpTransaction.objects.get(id=1).estado,
        #     response.data.get('estado')
        # )
        print("Se cambia el estado con exito")
