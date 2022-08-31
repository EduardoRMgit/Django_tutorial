# Para crear usuarios y transacciones con el token de esos usuarios
# en una pagina protegida por contraseñas
# se llama asi:
# python botnet.py <sufijo de usuario>

import sys
import requests
import json

moder = sys.argv[1]

numUsuarios = 20000
numTransaciones = 7
url = 'https://stage.zygoo.mx/graphql'

for x in range(numUsuarios):

    username = str(x) + moder
    password = x

    # Crear usuario
    query = """ mutation($username: String!, $password: String!){
      createUser(username:$username, password: $password){
        user{
          id
          username
          firstName
          lastName
        }
      }
    }
    """

    variables = {"username": "{}".format(username),
                 "password": "{}".format(password)}

    request = {"query": query, "variables": variables}
    header = {'Accept': 'application/json', 'Content-Type': 'application/json',
    		  'Authorization': 'Basic dGVzdDp0MzV0M3I='}

    r = requests.post(url=url, json=request, headers=header)

    for y in range(numTransaciones):

        # Autentificacion de Cactus
        query = """ mutation($username: String!, $password: String!){
                        tokenAuth(username: $username, password: $password){
                             token
                            }
                      }"""

        variables = {"username": "{}".format(username),
                     "password": "{}".format(password)}

        request = {"query": query, "variables": variables}
        header = {'Accept': 'application/json', 'Content-Type': 'application/json',
    		  'Authorization': 'Basic dGVzdDp0MzV0M3I='}

        r = requests.post(url=url, json=request, headers=header)
        resp = json.loads(r.content)
        token = resp['data']['tokenAuth']['token']

        # Create Transaccion
        header = {'Accept': 'application/json',
                  'Content-Type': 'application/json',
                  'Authorization': 'Basic dGVzdDp0MzV0M3I=',
                  'X-JWTToken': token}


        content = """
        mutation($monto: Decimal!, $comision: Decimal!){
          createTransaccion( monto: $monto, comision:$comision, comisionIVA:"12", pagadoMonto:"23", pagadoComision: "1999", pagadoComisionIVA: "25", porcentajeComision:"12", porcentajeComisionIVA:"12", fechaLiquidacion: "2019-07-31T00:01:04+00:00", productoId:1, statusTransId:1, tipoAnualId:1, statusCobranza:"V", statusVencimiento:"v"){
            id
            fechaTrans
            monto
            user {
              id
              isSuperuser
              username
              email
            }
            comision
            pagadoMonto
            porcentajeComisionIVA
          }
        }
        """
        monto = 10.00
        comision = 80.00
        variables = {"monto": monto,
                     "comision": comision}
        request = {"query": content, "variables": variables}

        r = requests.post(url=url, json=request, headers=header)
        print(r.text)
