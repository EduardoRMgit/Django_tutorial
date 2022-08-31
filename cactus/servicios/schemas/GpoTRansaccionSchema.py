import graphene
from graphene_django.types import DjangoObjectType
from servicios.models.transacciongpo import TransactionGpo
from servicios.models.productos import Productos
import requests
import json


class GpoTransaccionType(DjangoObjectType):
    class Meta:
        model = TransactionGpo


class GpoProductosType(DjangoObjectType):
    class Meta:
        model = Productos


class CreateTransaccionGpo(graphene.Mutation):
    # Gpo_transaccion = graphene.Field(GpoTransaccionType)
    valida = graphene.String()
    # user = graphene.Field()

    class Arguments:
        Servicio = graphene.String()
        Producto = graphene.String()
        Resp = graphene.String()
        Comision_GPO = graphene.String()
        Comision_BratD = graphene.String()
        Saldo_Cliente = graphene.String()
        ID_TX = graphene.String()
        Num_Aut = graphene.String()
        Referencia = graphene.String()
        Err = graphene.String()
        stat_code = graphene.String()
        Telefono = graphene.String()
        id_servicio = graphene.Int(required=True)
        id_producto = graphene.Int()
        Precio = graphene.String()

    def mutate(self,
               info,
               Servicio=None,
               Producto=None,
               Resp=None,
               Comision_GPO=None,
               Comision_BratD=None,
               Saldo_Cliente=None,
               ID_TX=None,
               Num_Aut=None,
               Referencia=None,
               Err=None,
               stat_code=None,
               Telefono=None,
               id_servicio=None,
               id_producto=None,
               Precio=None):
        # URL de token authentication
        url = 'http://167.99.25.139/GPOApp/api-token-auth/'
        # Ask for username and password
        input_name = 'aldo'
        input_pwd = 'Acurielm1'
        payload = {'username': input_name, 'password': input_pwd}
        headers = {'content-type': 'application/json'}
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
        except Exception as e:
            print(f'Error: {e} communicating to get token GPO')
        # Turn into a string
        rstring = r.content.decode('utf-8')
        try:
            token = json.loads(rstring)['token']
        except Exception as e:
            print(f"Response has no token {e}")
            return f"Response has no token {e}"
        url = 'http://167.99.25.139/GPOApp/transactions/'
        headers = {'Accept': 'application/json',
                   'Authorization':
                   f'Token {token}'}
        data = {'id': id_servicio, 'Telefono': Telefono}
        print("id_servicio MUTACION:", id_servicio)
        # Este id_servicio el "data={'id': id_servicio, 'Telefono': Telefono}"
        # lo lee como el "id" que es diferente al "id_servicio".
        try:
            r = requests.post(url, headers=headers, data=data)
        except Exception as e:
            print(f'{e} when doing trans')
        json_datatran = json.loads(r.content)
        dict_gpo = json_datatran['data_request']
        telefonotr = dict_gpo['telefono']
        # Nombre del Servicio:
        serv = Productos.objects.get(id=data['id'])
        # id_servicio:
        # idServicio = serv.id_servicio
        price = "200.00"
        errortrans = json_datatran['codigo']
        print("error code:", errortrans)
        if json_datatran['http'] == '200':
            TransactionGpo.objects.create(Telefono=telefonotr,
                                          Precio=price,
                                          Servicio=serv,
                                          Err=errortrans,
                                          )
            return CreateTransaccionGpo(json_datatran['codigo'])
        elif json_datatran['http'] == '406':
            TransactionGpo.objects.create(Telefono=telefonotr,
                                          Precio=price,
                                          Servicio=serv,
                                          Err=errortrans,
                                          )
            return CreateTransaccionGpo(json_datatran['codigo'])
        else:
            TransactionGpo.objects.create(Telefono=telefonotr,
                                          Precio=price,
                                          Servicio=serv,
                                          Err=errortrans,
                                          )
            return CreateTransaccionGpo(json_datatran['codigo'])


class Mutation(graphene.ObjectType):
    create_transaccion_gpo = CreateTransaccionGpo.Field()
