"""
<Nombre del programa>
  test_device.py
<Autor(a)>
  Damaris A. Zavala <damaris.zavala@erona.io>
<Iniciado>
  Oct 26, 2020
<Copyright>
  See LICENSE for licensing information.
<Propósito>
  Codigo para pruebas de mutaciones.
"""
from graphql_jwt.testcases import JSONWebTokenTestCase


class DeviceTest(JSONWebTokenTestCase):
    """
    Enrolamiento de Dispositivo (device).
        ---------------------------------------

        Se prueba en seis pasos la creación y desactivación de un dipositivo
        y los posibles errores dentro del enrolamiento correspondiente.
    """

    def test_create_device(self):
        """
        1 Mutación: createDevice
            - Con las variables en true y el uniqueId, comparamos que la
              respuesta de la mutación y la respuesta esperada, sean la misma
        2 Query: device
            - Constatamos que el nuevo dispositivo creado, con su respectiva
              pk, se encuentre activo.
        3 Mutación: createDevice <con variables erróneas>
            - Probamos que entregue el error esperado al declarar create:false.
              Comparamos que la respuesta de la mutación y la respuesta del
              error esperado, sean la misma
        4 Mutación: deleteDevice <con variables erróneas>
            - Probamos que entregue el error esperado al declarar una pk que no
              coincida con el device en cuestion.
              Comparamos que la respuesta de la mutación y la respuesta del
              error esperado, sean la misma.
        5 Mutación: deleteDevice
            - Con la pk especifica, comparamos que la respuesta de la mutación
              y la respuesta esperada, sean la misma.
        6 Query: device
            - Constatamos que el dispositivo desactivado con su respectiva
              pk, se encuentre inactivo.
        """
        mutation = '''
            mutation createDevice($create: Boolean!,
                                  $active: Boolean!,
                                  $uniqueId: String!){
                createDevice(create: $create,
                             active: $active,
                             uniqueId: $uniqueId){
                    device{
                    id
                    active
                    }
                }
                }
        '''
        variables = {"create": True,
                     "active": True,
                     "uniqueId": "666"}
        res = self.client.execute(mutation, variables)
        expected_res = {
                "createDevice": {
                    "device": {
                        "id": "1",
                        "active": True
                         }
                    }
                }
        self.assertEqual(res.data, expected_res)
        print(" [assert OK] Device created  ")

        # 2. Revisar en query que este activo
        query = '''
            query device($pk: Int!){
                device(pk: $pk){
                    active
                }
            }
        '''
        # pk:1 corresponde a device creado para enrolamiento de test
        variables4 = {'pk': 1}
        res4 = self.client.execute(query, variables4)
        self.assertEqual(res4.data['device']['active'], True)

        # 3. Ahora el (test)' de createDevice <con create: false>
        variables2 = {"create": False,
                      "active": True,
                      "uniqueId": "666"}
        res2 = self.client.execute(mutation, variables2)
        self.assertEqual(res2.data['createDevice'], None)
        self.assertEqual(res2.errors[0].message,
                         'UserDevice matching query does not exist.')
        print(" [assert OK] Device not created  ")

        # 4. Mutacion delete device
        mutation2 = '''
            mutation deleteDevice($pk: Int!){
                deleteDevice(pk: $pk){
                    ok
                }
                }
        '''
        # Probamos delete device con datos incorrectos
        variables3 = {"pk": "3"}
        res3 = self.client.execute(mutation2, variables3)

        self.assertEqual(res3.data['deleteDevice'], None)
        self.assertEqual(res3.errors[0].message,
                         'UserDevice matching query does not exist.')

        # 5. Probamos delete device con datos correctos
        variables2 = {"pk": "1"}
        res2 = self.client.execute(mutation2, variables2)
        expected_res2 = {
            "deleteDevice": {
                "ok": True
                }
            }
        self.assertEqual(res2.data, expected_res2)
        print(" [assert OK] Device deleted  ")

        # 6. Revisar en query que este inactivo
        query = '''
            query device($pk: Int!){
                device(pk: $pk){
                    active
                }
            }
        '''
        # Se borra pk:1 corresponde a device creado para camino de test
        variables4 = {'pk': 1}
        res4 = self.client.execute(query, variables4)
        self.assertEqual(res4.data['device']['active'], False)
