import requests
import json

# url = 'http://192.168.15.26:8000/graphql'
# username = "aldo"
# password = "Acurielm1"
#
# # Autentificacion de Cactus
# query = """ mutation($username: String!, $password: String!){
#                 tokenAuth(username: $username, password: $password){
#                      token
#                     }
#               }"""
#
# variables = {"username": "{}".format(username),
#              "password": "{}".format(password)}
#
# request = {"query": query, "variables": variables}
# header = {'Accept': 'application/json', 'Content-Type': 'application/json'}
#
# r = requests.post(url=url, json=request, headers=header)
# resp = json.loads(r.content)
# token = resp['data']['tokenAuth']['token']
#
# print(token)
#
# # Create Transaccion
# header = {'Accept': 'application/json',
#           'Content-Type': 'application/json',
#           'Authorization': 'jwt {}'.format(token)}
#
#
# content = """
# mutation($monto: Decimal!, $comision: Decimal!){
#   createTransaccion( monto: $monto, comision:$comision, comisionIVA:"12", pagadoMonto:"23", pagadoComision: "1999", pagadoComisionIVA: "25", porcentajeComision:"12", porcentajeComisionIVA:"12", fechaLiquidacion: "2019-07-31T00:01:04+00:00", productoId:1, statusTransId:1, tipoAnualId:1, statusCobranza:"V", statusVencimiento:"v"){
#     id
#     fechaTrans
#     monto
#     user {
#       id
#       isSuperuser
#       username
#       email
#     }
#     comision
#     pagadoMonto
#     porcentajeComisionIVA
#   }
# }
# """
# monto = 10.00
# comision = 80.00
# variables = {"monto": monto,
#              "comision": comision}
# request = {"query": content, "variables": variables}
#
# r = requests.post(url=url, json=request, headers=header)
# print(r.text)
#
# # DDE transaccion
# url = 'http://192.168.15.26:8001/graphql'
# query = """
# mutation{
#   createTransaccion(user:"7",monto:"15.0022", comision:"12", comisionIVA:"12", pagadoMonto:"23", pagadoComision: "1999", pagadoComisionIVA: "25", porcentajeComision:"12", porcentajeComisionIVA:"12", fechaLiquidacion: "2019-07-31T00:01:04+00:00", fechaVencimiento: "2019-08-31T00:01:04+00:00",,productoId:1, statusTransId:1, tipoAnualId:1, statusCobranza:"V", statusVencimiento:"v"){
#     id
#     fechaTrans
#     monto
#     user {
#       id
#       isSuperuser
#       username
#       email
#     }
#     comision
#     pagadoMonto
#     porcentajeComisionIVA
#   }
# }
# """
#
# request = {"query": query}
# header = {'Accept': 'application/json', 'Content-Type': 'application/json'}
# r = requests.post(url=url, json=request, headers=header)
# print(r.text)

numUsuarios = 150000
numTransaciones = 7
url = 'https://zygoo.mx/graphql'

for x in range(numUsuarios):

    username = x
    password = x

    # Autentificacion de Cactus
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
    header = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    r = requests.post(url=url, json=request, headers=header)
    print(r.text)

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
        header = {'Accept': 'application/json', 'Content-Type': 'application/json'}

        r = requests.post(url=url, json=request, headers=header)
        resp = json.loads(r.content)
        token = resp['data']['tokenAuth']['token']

        # Create Transaccion
        header = {'Accept': 'application/json',
                  'Content-Type': 'application/json',
                  'Authorization': 'jwt {}'.format(token)}


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
