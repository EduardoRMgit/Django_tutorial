import graphene
from graphene_django.types import DjangoObjectType
from pagos.rapydcollect.models import (Payment, RequiredFields,
                                       PaymentRequiredFields,
                                       MetodosdepagoPais,
                                       Paises)
from pagos.utilities import make_request
from graphene_django.converter import convert_django_field
from jsonfield import JSONField
from graphene import String, List
from demograficos.models.userProfile import UserProfile
from spei.stpTools import randomString
import json
from graphql_jwt.decorators import login_required
from django.contrib.auth.models import User
from django_countries.fields import Country


@convert_django_field.register(JSONField)
def convert_field_to_string(field, registry=None):
    return List(String, source='get_tags')


class UProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile


class PaispagosType(DjangoObjectType):
    class Meta:
        model = MetodosdepagoPais


class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment


class RequiredFieldsType(DjangoObjectType):
    class Meta:
        model = RequiredFields


class PaymentMethodRequiredFieldsType(DjangoObjectType):
    class Meta:
        model = PaymentRequiredFields


class CollectUserType(DjangoObjectType):
    class Meta:
        model = User


class GetPaymentMethodByCountrys(graphene.Mutation):

    metodosdepago = graphene.List(PaispagosType)

    class Arguments:
        token = graphene.String(required=False)

    @login_required
    def mutate(self, info, token):

        if info.context.user.is_anonymous:
            return None

        pais = "mx"
        r = make_request(method='get',
                         path='/v1/payment_methods/country?country=' + pais)
        n = len(r["data"])
        nuevoarray = []
        co = Country(pais)
        pa, _ = Paises.objects.get_or_create(nombre=co)
        for i in range(0, n):
            gl, _ = MetodosdepagoPais.objects.get_or_create(nombre=r["data"][i]["type"], pais=pa)  # noqa: E501
            nuevoarray.append(gl)

        return GetPaymentMethodByCountrys(metodosdepago=nuevoarray)


class Query(graphene.ObjectType):
    """
    ---- allMethodRequiredFields ----

    * Caso 1: Si tiene campos requeridos
    query{
      allMethodRequiredFields(banco: "mx_mastercard_card", token:"token")
    }

    >>> Respuesta 1
      "data": {
        "allMethodRequiredFields": [
          "{'name': 'number', 'type': 'string', 'regex': '', 'is_required': True, 'instructions': 'card number'}",  # noqa: E501
          "{'name': 'expiration_month', 'type': 'string', 'regex': '', 'is_required': True, 'instructions': 'expiration month as string, 01-12'}",  # noqa: E501
          "{'name': 'expiration_year', 'type': 'string', 'regex': '', 'is_required': True, 'instructions': 'expiration year in to digits as string, 18-99'}",  # noqa: E501
          "{'name': 'cvv', 'type': 'string', 'regex': '', 'is_required': True, 'instructions': 'card cvv'}",  # noqa: E501
          "{'name': 'name', 'type': 'string', 'regex': '', 'is_required': False, 'instructions': 'card holder name'}"  # noqa: E501
        ]
      }

    * Caso 2: Respuesta en caso de no tener campos requeridos
    query{
      allMethodRequiredFields(banco: "mx_diestel_cash", token:"token")
    }

    >>> Respuesta 2
      "data": {
        "allMethodRequiredFields": []
      }
    """

    """
    ---- pagosdeusuario ----

    query{
        pagosdeusuario(token: "token"){
            id
            user {
                id
                username
            }
            amount
            fechaPago
        }
    }

    >>> Respuesta
    "data": {
        "pagosdeusuario": [
        {
            "id": "1",
            "user": {
                "id": "1",
                "username": "admin"
            },
            "amount": 12200,
            "fechaPago": "2021-04-15T02:45:08.510000+00:00"
        },
        {
            "id": "2",
            "user": {
                "id": "1",
                "username": "admin"
            },
            "amount": 25000,
            "fechaPago": "2021-04-15T02:47:42.173000+00:00"
        },
        {
            "id": "3",
            "user": {
                "id": "1",
                "username": "admin"
            },
            "amount": 7600,
            "fechaPago": "2021-04-15T02:48:48.532000+00:00"
        },
        {
            "id": "4",
            "user": {
                "id": "1",
                "username": "admin"
            },
            "amount": 300,
            "fechaPago": "2021-04-15T02:49:59.258000+00:00"
        }
    ]
    }

    >>> Respuesta token no válido
        "errors": [
        {
        "message": "Error decoding signature",
        "locations": [
            {
            "line": 2,
            "column": 3
            }
        ],
        "path": [
            "pagosdeusuario"
        ]
        }
        ],
        "data": {
            "pagosdeusuario": null
        }
    """

    all_method_required_fields = graphene.List(graphene.String,
                                               banco=graphene.String(required=True),   # noqa: E501
                                               token=graphene.String(required=True),)   # noqa: E501
    pagosdeusuario = graphene.List(PaymentType,
                                   token=graphene.String(required=True))

    @login_required
    def resolve_pagosdeusuario(self, info, **kwargs):
        user = info.context.user
        pagosdeusuario = Payment.objects.filter(user=user)
        return pagosdeusuario

    @login_required
    def resolve_all_method_required_fields(self, info, banco, **kwargs):
        path = '{}{}'.format('/v1/payment_methods/required_fields/', banco)
        r = make_request(method='get',
                         path=path
                         )
        json.dumps(r)
        return r['data']['fields']


class CreatePayment(graphene.Mutation):
    """
    CreatePayment (Mutation): Crea un pago de usuario requiriendo su token,
    monto, método de pago, nip y descripción. Por medio
    del token se complementan los datos del usuario.
    Se asigna un código de pago (merchant reference id) para algunos casos
    conocidos.


    Arguments:
        token = String(required)
        monto = Int
        metodo_pago = String
        description = String
        merchant_reference_id = graphene.String()
        nip = graphene.String(required=True)

    >>> Mutation Example:

    mutation{
        createPayment(token:"token",
                      monto:100000,
                      metodoPago:"mx_diestel_cash",
                      description:"ejemplo",
                      merchant_reference_id: "ejemplo",
                      nip: "nip" ){
                createPayment{
                id
                status
                responseCode
                idPayment
                amount
                statusData
                payCode
                textualCodes
                user{
                    username
                }
            }
        }
    }

    >>> Response:
   {
    "data": {
        "createPayment": {
        "createPayment": {
            "id": "6",
            "status": "",
            "responseCode": "",
            "idPayment": "payment_cabad9d17dce4f379851a758c4eae7a2",
            "amount": 100000,
            "statusData": "ACT",
            "payCode": "8230391236750788",
            "textualCodes": null,
            "user": {
            "username": "aaaa"
            }
        }
        }
    }
    }
    """

    create_payment = graphene.Field(PaymentType)
    profile = graphene.Field(UProfileType)

    class Arguments:
        token = graphene.String(required=True)
        monto = graphene.Int()
        metodo_pago = graphene.String()
        description = graphene.String()
        merchant_reference_id = graphene.String()
        nip = graphene.String(required=True)

    @login_required
    def mutate(self,
               info,
               token,
               nip,
               monto=None,
               metodo_pago=None,
               description=None,
               merchant_reference_id=None
               ):

        user = info.context.user
        if user.is_anonymous:
            return
        if not user.Uprofile.check_password(nip):
            raise Exception('Nip esta mal')

        payment_body = {
                        "amount": monto,
                        "currency": "MXN",
                        "merchant_reference_id": merchant_reference_id,
                        "description": description,
                        "payment_method": {
                            "type": metodo_pago
                            }
                        }

        user = info.context.user

        response = make_request(method='post', path='/v1/payments', body=payment_body)  # noqa: E501

        # Assign code from some known cases, if it is not one of those case
        # assign None
        paycode = None
        try:
            paycode = response['data']['textual_codes']['paycode']
        except Exception:
            pass

        try:
            paycode = response['data']['textual_codes']['pay_code']
        except Exception:
            pass

        try:
            paycode = response['data']['textual_codes']['pairing_code']
        except Exception:
            pass

        try:
            paycode = response['data']['textual_codes']['payment_code']
        except Exception:
            pass

        try:
            paycode = response['data']['textual_codes']['code']
        except Exception:
            pass

        try:
            paycode = response['data']['visual_codes']['payCode']
        except Exception:
            pass

        claveR = randomString()

        create_payment = Payment(user=user,
                                 amount=monto,
                                 payment_method=metodo_pago,
                                 status='ACT',
                                 operation_id=response['status']['operation_id'],  # noqa: E501
                                 idPayment=response['data']['id'],
                                 currency_code=response['data']['currency_code'],  # noqa: E501
                                 statusData=response['data']['status'],
                                 description=response['data']['description'],
                                 merchant_reference_id=response['data']['merchant_reference_id'],  # noqa: E501
                                 payCode=paycode,
                                 claveRastreoR=claveR
                                 )
        create_payment.save()

        return CreatePayment(
            create_payment=create_payment
        )


class Mutation(graphene.ObjectType):

    get_pay_for_country = GetPaymentMethodByCountrys.Field()
    create_payment = CreatePayment.Field()
