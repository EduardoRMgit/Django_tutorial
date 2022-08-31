import graphene
from graphene_django.types import DjangoObjectType
from demograficos.models.tarjeta import StatusTarjeta, Tarjeta


class StatusTarjetaType(DjangoObjectType):
    class Meta:
        model = StatusTarjeta


class TarjetaType(DjangoObjectType):
    class Meta:
        model = Tarjeta


class Query(object):
    """
    ``statusTarjeta (Query): Query a single object from StatusTelefono \
Model``

        Arguments:
            - statusId(int): pk from the StatusTarjeta model object
            - status (string): A valid status of StatusTarjeta model

        Fields to query:
            - id
            - status
            - tarjetaSet

    >>> Query Example:
    query{
        statusTarjeta(status:"Vigente"){
            id
            status
            tarjetaSet{
                id
            }
        }
    }

    >>> Response:
    {
        "data": {
            "statusTarjeta": {
            "id": "1",
            "status": "Vigente",
            "tarjetaSet": [
                    {
                        "id": "1"
                    },
                    {
                        "id": "2"
                    }
                ]
            }
        }
    }


    ``allStatusTarjeta (Query): Query all objects from StatusTelefono \
Model``

        Arguments:
            - None

        Fields to query:
            - Same from statusTarjeta query

    >>> Query Example:
    query{
        allStatusTarjeta{
            id
            status
        }
    }

    >>> Response:
    {
        "data": {
            "allStatusTarjeta": [
                {
                    "id": "1",
                    "status": "Vigente"
                },
                {
                    "id": "2",
                    "status": "Expirada"
                },
                {
                    "id": "3",
                    "status": "Por Expirar"
                }
            ]
        }
    }


    ``tarjeta (Query): Query a single object from Tarjeta Model``

        Arguments:
            - tarjetaId (int): pk from the Tarjeta Model object
            - tarjeta (string): user's card number

        Fields to query:
            - id
            - tarjetaDebitoNum
            - tarjetaDebitoPin
            - country
            - user
            - institucion
            - statusTarjeta

    >>> Query Example:
    query {
        tarjeta(tarjetaId: 2) {
            id
            tarjetaDebitoNum
            tarjetaDebitoPin
            country
            user {
                id
            }
            institucion {
                id
            }
            statusTarjeta {
                id
            }
        }
    }


    >>> Response:
    {
        "data": {
            "tarjeta": {
            "id": "2",
            "tarjetaDebitoNum": "4562145874589658",
            "tarjetaDebitoPin": "854",
            "country": "MX",
            "user": {
                    "id": "3"
                },
            "institucion": {
                    "id": "1"
                },
            "statusTarjeta": {
                    "id": "1"
                }
            }
        }
    }

    ``allTarjeta (Query): Query all objects from Tarjeta Model``

        Arguments:
            - None

        Fields to query:
            - Same from tarjeta query

    >>> Query Example:
    query {
        allTarjeta {
            id
            tarjetaDebitoNum
            tarjetaDebitoPin
            country
        }
    }



    >>> Response:
    {
        "data": {
            "allTarjeta": [
                {
                    "id": "1",
                    "tarjetaDebitoNum": "4555789545786589",
                    "tarjetaDebitoPin": "452",
                    "country": "MX"
                },
                {
                    "id": "2",
                    "tarjetaDebitoNum": "4562145874589658",
                    "tarjetaDebitoPin": "854",
                    "country": "MX"
                }
            ]
        }
    }

"""
    status_tarjeta = graphene.Field(StatusTarjetaType,
                                    status_id=graphene.Int(),
                                    status=graphene.String(),
                                    description="`Query a single object from \
                                    StatusTelefono Model:` using statusId(pk) \
                                    or status (string)")
    all_status_tarjeta = graphene.List(StatusTarjetaType,
                                       description="`Query all objects from \
                                           StatusTarjeta model`")

    tarjeta = graphene.Field(TarjetaType,
                             tarjeta_id=graphene.Int(),
                             tarjeta=graphene.String(),
                             description="`Query a single object from \
                                Tarjeta Model:` using tarjetaId(pk) \
                                or tarjeta (string)")
    all_tarjeta = graphene.List(TarjetaType,
                                description="`Query all objects from \
                                    Tarjeta model`")

    def resolve_all_status_tarjeta(self, info, **kwargs):
        return StatusTarjeta.objects.all()

    def resolve_all_tarjeta(self, info, **kwargs):
        return Tarjeta.objects.all()

    def resolve_status_tarjeta(self, info, **kwargs):
        id = kwargs.get('status_id')
        status = kwargs.get('status')

        if id is not None:
            return StatusTarjeta.objects.get(pk=id)

        if status is not None:
            return StatusTarjeta.objects.get(status=status)

    def resolve_tarjeta(self, info, **kwargs):
        id = kwargs.get('tarjeta_id')
        status = kwargs.get('status')

        if id is not None:
            return Tarjeta.objects.get(pk=id)

        if status is not None:
            return Tarjeta.objects.get(status=status)
