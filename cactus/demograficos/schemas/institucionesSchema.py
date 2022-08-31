from graphene_django.types import DjangoObjectType
import graphene
from demograficos.models.instituciones import Institucion


class InstitucionType(DjangoObjectType):
    class Meta:
        model = Institucion


class Query(object):
    """

    ``institucion (Query): Query a single object from Institucion Model``

        Arguments:
            - institucionId (int): pk from the Institucion Model object
            - nombre (string): Institution's name

        Fields to query:
            - id
            - nombre
            - limiteCredito
            - minPorcentaje
            - maxPorcentaje
            - user
            - country
            - tarjetaSet
            - productosSet
            - transpagoAuthheadSet

        >>> Query Example:
    query{
        institucion(nombre:"Banamex"){
            id
            nombre
            limiteCredito
            minPorcentaje
            maxPorcentaje
            user {
                id
            }
            country
            tarjetaSet {
                id
            }
            productosSet {
                id
            }
            transpagoAuthheadSet {
                id
            }
        }
    }

        >>> Response:
    {
    "data": {
            "institucion": {
            "id": "2",
            "nombre": "Banamex",
            "limiteCredito": 2800,
            "minPorcentaje": 10,
            "maxPorcentaje": 15,
            "user": [],
            "country": "MX",
            "tarjetaSet": [],
            "productosSet": [
            {
            "id": "2"
            }
            ],
            "transpagoAuthheadSet": []
            }
        }
    }

    ``allInstitucion (Query): Query all objects from Institucion Model``

        Arguments:
            - None

        Fields to query:
            - Same from institucion query

        >>> Query Example:
    query{
        allInstitucion {
            id
            nombre
        }
    }


        >>> Response:
    {
        "data": {
            "allInstitucion": [
                {
                    "id": "1",
                    "nombre": "Santander"
                },
                {
                    "id": "2",
                    "nombre": "Banamex"
                }
            ]
        }
    }

    """

    institucion = graphene.Field(InstitucionType,
                                 institucion_id=graphene.Int(),
                                 nombre=graphene.String(),
                                 description="`Query a single object from \
                                 Institucion Model:` using institucionId(pk) \
                                 or nombre (string)")
    all_institucion = graphene.List(InstitucionType,
                                    description="`Query all objects \
                                    from Institucion Model`")

    # Initiating Resolvers
    def resolve_all_institucion(self, info, **kwargs):
        return Institucion.objects.all()

    def resolve_institucion(self, info, **kwargs):

        id = kwargs.get('institucion_id')
        nombre = kwargs.get('nombre')

        if id is not None:
            return Institucion.objects.get(pk=id)

        if nombre is not None:
            return Institucion.objects.get(nombre=nombre)
