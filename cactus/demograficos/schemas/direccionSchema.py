import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required
from demograficos.models.direccion import (TipoDireccion,
                                           EntidadFed,
                                           Direccion,
                                           Country)
from demograficos.models.telefono import Telefono
from demograficos.models.profileChecks import InfoValidator, ComponentValidated
from pld.utils.customerpld import update_pld_customer
from demograficos.utils.tokendinamico import tokenD


class TipoDireccionType(DjangoObjectType):
    class Meta:
        model = TipoDireccion


class EntidadFedType(DjangoObjectType):
    class Meta:
        model = EntidadFed


class DireccionType(DjangoObjectType):
    class Meta:
        model = Direccion


class CountryType(DjangoObjectType):
    class Meta:
        model = Country


class UserTelefonoType(DjangoObjectType):
    class Meta:
        model = Telefono


class ComponentType(DjangoObjectType):
    class Meta:
        model = ComponentValidated


class Query(object):
    """

    ``tipoDireccion (Query): Query a single object from TipoDireccion Model``

        Arguments:
            - direccionId (int): pk from the Direccion Model Object
            - tipo (string): Adress kinde of the user.

        Fields to query:
            - id
            - tipo
            - direccionSet

    >>> Query Example:
    query{
        tipoDireccion(direccionId:1){
            id
            tipo
            direccionSet {
                id
            }
        }
    }

    >>> Response:
    {
        "data": {
            "tipoDireccion": {
            "id": "1",
            "tipo": "Casa",
            "direccionSet": [
                {
                    "id": "1"
                },
                {
                    "id": "3"
                },
                {
                    "id": "4"
                }
            ]
            }
        }
    }


    ``allTipoDireccion (Query): Query all objects from TipoDireccion Model``

        Arguments:
            - None

        Fields to query:
            - Same from tipoDireccion query

    >>> Query Example:
    query {
        allTipoDireccion{
            id
            tipo
        }
    }

    >>> Response:
    {
        "data": {
            "allTipoDireccion": [
            {
                "id": "1",
                "tipo": "Casa"
            },
            {
                "id": "2",
                "tipo": "Oficina"
            }
            ]
        }
    }


    ``entidadFed (Query): Query a single object from EntidadFed Model``

        Arguments:
            - entidadFedId (int): pk of the EntidadFed model object
            - entidad (string): State of Mexico

        Fields to query:
            - id
            - entidad
            - direccionSet

    >>> Query Example:
    query{
        entidadFed(entidadFedId:1){
            id
            entidad
        }
    }

    >>> Response:
    {
        "data": {
            "entidadFed": {
            "id": "1",
            "entidad": "CDMX"
            }
        }
    }



    ``allEntidadFed (Query): Query all objects from EntidadFed Model``

        Arguments:
            - None

        Fields to query:
            - Same from entidadFed query

    >>> Query Example:
    query{
        allEntidadFed{
            id
            entidad
        }
    }

    >>> Response:
    {
        "data": {
            "allEntidadFed": [
                {
                    "id": "1",
                    "entidad": "CDMX"
                },
                {
                    "id": "2",
                    "entidad": "Qro"
                }
            ]
        }
    }



    ``direccion (Query): Query a single object from Direccion Model``

        Arguments:
            - direccionId (int): pk of the Direccion Model object.

        Fields to query:
            - id
            - linea1
            - linea2
            - codPostal
            - ciudad
            - delegMunicipio
            - fechaCreacion
            - activo
            - validado
            - country
            - user
            - tipoDireccion
            - entidadFed

    >>> Query Example:
    query{
        direccion(direccionId:1){
            id
            linea1
            linea2
            codPostal
            ciudad
            delegMunicipio
            fechaCreacion
            activo
            validado
            country
            user {
                id
            }
            tipoDireccion {
                id
            }
            entidadFed {
                id
            }
        }
    }

    >>> Response:
    {
        "data": {
            "direccion": {
                "id": "1",
                "linea1": "Comoporis 189",
                "linea2": "Col. El Reloj",
                "codPostal": "02030",
                "ciudad": "Ciudad Azteca",
                "delegMunicipio": "Coyoacan",
                "fechaCreacion": "2019-08-16T01:53:35+00:00",
                "activo": true,
                "validado": true,
                "country": "MX",
                "user": {
                    "id": "5"
                },
                "tipoDireccion": {
                    "id": "1"
                },
                "entidadFed": {
                    "id": "1"
                }
            }
        }
    }


    ``allDireccion (Query): Query all objects from Direccion Model``

        Arguments:
            - None

        Fields to query:
            - Same from direccion query

    >>> Query Example:
    query{
        allDireccion{
            id
            linea1
        }
    }

    >>> Response:
    {
        "data": {
            "allDireccion": [
                {
                    "id": "1",
                    "linea1": "Comoporis 189"
                },
                {
                    "id": "2",
                    "linea1": "Av Coyoacán 1435 Edificio A Local 5"
                },
                {
                    "id": "3",
                    "linea1": "Rancho Piomo 889"
                },
                {
                    "id": "4",
                    "linea1": "Prado del Norte"
                }
            ]
        }
    }

    """
    tipo_direccion = graphene.Field(TipoDireccionType,
                                    direccion_id=graphene.Int(),
                                    tipo=graphene.String(),
                                    description="`Query a single object from \
                                        TipoDireccion Model:` using \
                                        direccionId(pk) or tipo(string)")
    all_tipo_direccion = graphene.List(TipoDireccionType,
                                       description="`Query all objects from \
                                           TipoDireccion Model`")

    entidad_fed = graphene.Field(EntidadFedType,
                                 entidad_fed_id=graphene.Int(),
                                 entidad=graphene.String(),
                                 description="`Query a single object from \
                                    EntidadFed Model:` using \
                                    entidadFedId(pk) or entidad(string)")
    all_entidad_fed = graphene.List(EntidadFedType,
                                    description="`Query all objects from \
                                        EntidadFed Model`")

    direccion = graphene.List(DireccionType,
                              token=graphene.String(required=False),
                              direccion_id=graphene.Int(),
                              user_id=graphene.Int(),
                              description="`Query a single object from \
                                Direccion Model:` using direccionId(pk)"
                              )
    all_direccion = graphene.List(DireccionType,
                                  description="`Query all objects from \
                                    Direccion Model`")

    user_telefono = graphene.Field(UserTelefonoType,
                                   userid=graphene.Int(),
                                   username=graphene.String(),
                                   telefono=graphene.String(),
                                   description="`Query a single object from \
                                     the beneficiarios model`")

    all_countries = graphene.List(CountryType,
                                  description="`Query all objects from \
                                    EntidadFed Model`")

    def resolve_all_tipo_direccion(self, info, **kwargs):
        return TipoDireccion.objects.all()

    def resolve_all_entidad_fed(self, info, **kwargs):
        return EntidadFed.objects.all()

    def resolve_all_direccion(self, info, **kwargs):
        return Direccion.objects.all()

    def resolve_all_user_telefono(self, info, **kwargs):
        return Telefono.objects.all()

    def resolve_all_countries(self, info, **kwargs):
        return Country.objects.all()

    # RESOLVE EACH TYPE
    def resolve_tipo_direccion(self, info, **kwargs):
        id = kwargs.get('direccion_id')
        tipo = kwargs.get('tipo')

        if id is not None:
            return TipoDireccion.objects.get(pk=id)

        if tipo is not None:
            return TipoDireccion.objects.get(tipo=tipo)

        return None

    def resolve_entidad_fed(self, info, **kwargs):
        id = kwargs.get('entidad_fed_id')
        entidad = kwargs.get('entidad')

        if id is not None:
            return EntidadFed.objects.get(pk=id)

        if entidad is not None:
            return EntidadFed.objects.get(entidad=entidad)

        return None

    @login_required
    def resolve_direccion(self, info, **kwargs):
        # uid = kwargs.get('user_id')
        #
        # if uid is not None:
        #     return Direccion.objects.get(pk=uid)
        user = info.context.user
        if not user.is_anonymous:
            direccion = user.user_direccion.filter(activo=True)
            return direccion

        return None

    def resolve_user_telefono(self, info, **kwargs):
        id = kwargs.get('userid')

        if id is not None:
            temp = User.objects.get(pk=id)
            return temp.user_telefono.all()
        return None


class setDireccion(graphene.Mutation):

    direccion = graphene.Field(DireccionType)
    validities = graphene.List(ComponentType)

    class Arguments:
        token = graphene.String(required=True)
        edit = graphene.Boolean()
        calle = graphene.String()
        num_int = graphene.String()
        num_ext = graphene.String()
        codPostal = graphene.String()
        tipo_direccion = graphene.Int()
        colonia = graphene.String()
        alcaldiaMunicipio = graphene.String()
        estado = graphene.Int()
        ciudad = graphene.String()

    def mutate(
            self, info, token, edit=False, calle=None,
            codPostal=None, tipo_direccion=1, ciudad=None,
            alcaldiaMunicipio=None, num_int=None, num_ext=None, colonia=None,
            estado=None, country='MX'):

        try:
            entidad = EntidadFed.objects.get(pk=estado)
        except Exception:
            entidad = EntidadFed.objects.get(pk=1)
        try:
            tipo_direccion = TipoDireccion.objects.get(pk=tipo_direccion)
        except Exception:
            tipo_direccion = TipoDireccion.objects.get(pk=1)

        dir_dict = {'codPostal': codPostal, 'tipo_direccion': tipo_direccion,
                    'ciudad': ciudad, 'delegMunicipio': alcaldiaMunicipio,
                    'num_int': num_int, 'num_ext': num_ext,
                    'colonia': colonia, 'entidadFed': entidad,
                    'country': country}
        user = info.context.user
        if not user.is_anonymous:
            dirs = user.user_direccion.filter(activo=True)
            if edit:
                try:
                    dirs = user.user_direccion.filter(activo=True)
                    dir = dirs[0]
                except Exception as e:
                    raise Exception('no hay direcciones activas', e)
                dirs.update(**dir_dict)
                message = InfoValidator.setCheckpoint(
                                            user=user,
                                            concepto='DIR',
                                            data=dir_dict)
                if message == 'cp invalido':
                    raise Exception(message)
                try:
                    validities = ComponentValidated.objects.filter(
                                                                user=user)
                except Exception as e:
                    raise Exception(e)
                return setDireccion(direccion=dir, validities=validities)

            for dir in dirs:  # se desactivan las otras direcciones registradas
                dir.activo = False
                dir.save()

            direccion = (Direccion.
                         objects.create(
                                        calle=calle,
                                        num_int=num_int,
                                        num_ext=num_ext,
                                        codPostal=codPostal,
                                        ciudad=ciudad,
                                        delegMunicipio=alcaldiaMunicipio,
                                        user=user,
                                        entidadFed=entidad,
                                        colonia=colonia,
                                        tipo_direccion=tipo_direccion,
                                        activo=True))
            message = InfoValidator.setCheckpoint(user=user, concepto='DIR',
                                                  data=dir_dict)
            if message == 'cp invalido':
                raise Exception(message)
            try:
                validities = ComponentValidated.objects.filter(user=user)
            except Exception as e:
                raise Exception(e)
            return setDireccion(direccion=direccion, validities=validities)


class deleteDireccion(graphene.Mutation):
    """
    ``deleteDireccion (Mutation): Deactivates a Direccion``

    Arguments:
        -id (to identify the associated user)

    Fields to query:
        -

    >>> Mutation Example:


    >>> Response:


    """

    direccion = graphene.Field(DireccionType)

    class Arguments:
        id = graphene.Int()
        token = graphene.String(required=True)

    def mutate(self, info, token, id=None):
        user = info.context.user
        if not user.is_anonymous:
            dir = user.user_direccion.filter(activo=True)[0]
            dir.activo = False
            dir.save()
        return deleteDireccion(direccion=dir)


class CreateDireccion(graphene.Mutation):

    direccion = graphene.Field(DireccionType)

    class Arguments:

        token = graphene.String(required=True)
        token_d = graphene.String(required=True)
        calle = graphene.String()
        num_int = graphene.String()
        num_ext = graphene.String()
        codPostal = graphene.String()
        colonia = graphene.String()
        alcaldiaMunicipio = graphene.String()
        estado = graphene.String()

    def mutate(self, info, token, token_d, calle=None, codPostal=None,
               num_int=None, num_ext=None, colonia=None,
               alcaldiaMunicipio=None, estado=None):

        user = info.context.user
        dinamico = tokenD()
        if user.is_anonymous:
            raise Exception('User does not exist')
        if not dinamico.verify(token_d):
            raise Exception('token dinamico incorrecto')
        direccion = Direccion.objects.create(
            calle=calle,
            num_int=num_int,
            num_ext=num_ext,
            codPostal=codPostal,
            delegMunicipio=alcaldiaMunicipio,
            colonia=colonia,
            user=user,
            estado=estado,
            activo=True)
        update_pld_customer(user, direccion)
        Direccion.objects.filter(
            activo=True, user=user).update(activo=False)
        direccion.activo = True
        direccion.save()
        return CreateDireccion(direccion=direccion)


class Mutation(graphene.ObjectType):
    set_direccion = setDireccion.Field()
    delete_direccion = deleteDireccion.Field()
    create_direccion = CreateDireccion.Field()
