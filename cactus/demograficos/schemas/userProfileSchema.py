# flake8: noqa
import logging
import graphene
import datetime
import json
import os

from re import U
from random import randint

from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import get_token

from django.core.validators import validate_email

from django.db.models import Q

from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpRequest
from django.contrib.auth.models import User
from demograficos.models import GeoLocation, GeoDevice, UserLocation
from crecimiento.models import Respaldo
from django.contrib.auth import authenticate
from django.utils import timezone
from spei.stpTools import randomString
from django.conf import Settings
from geopy.geocoders import Nominatim


from demograficos.models.userProfile import (RespuestaSeguridad,
                                             PreguntaSeguridad,
                                             UserProfile,
                                             StatusRegistro,
                                             StatusCuenta,
                                             IndiceDisponible,
                                             UserNotas,
                                             HistoriaLinea,
                                             UserDevice,
                                             UserBeneficiario,
                                             NipTemporal,
                                             INE_Info,
                                             INE_Reg_Attempt,
                                             RestorePassword,
                                             Parentesco,
                                             Avatar)
from demograficos.models.telefono import Telefono
from demograficos.models.contactos import Contacto
from demograficos.models.profileChecks import (ComponentValidated,
                                               ProfileComponent,
                                               InfoValidator,
                                               register_device)
from demograficos.models.documentos import (DocAdjunto, DocAdjuntoTipo,
                                            DocExtraction)
from demograficos.models.perfildeclarado import (TransferenciasMensuales,
                                                 OperacionesMensual,
                                                 UsoCuenta,
                                                 OrigenDeposito,
                                                 PerfilTransaccionalDeclarado,)

from banca.models.entidades import CodigoConfianza
from banca.utils.clabe import es_cuenta_inguz

from spei.models import InstitutionBanjico

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from axes.models import AccessAttempt

from pld.utils.customerpld import create_pld_customer

from demograficos.utils.registermail import RegistrarMail

db_logger = logging.getLogger("db")

# WRAPPERS


class RespuestaType(DjangoObjectType):
    class Meta:
        model = RespuestaSeguridad


class PreguntaType(DjangoObjectType):
    class Meta:
        model = PreguntaSeguridad


class TrueUserType(DjangoObjectType):
    class Meta:
        model = User


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile

    country = graphene.String()

    def resolve_country(self, info):
        return self.country.name


class StatusRegistroType(DjangoObjectType):
    class Meta:
        model = StatusRegistro


class StatusCuentaType(DjangoObjectType):
    class Meta:
        model = StatusCuenta


class IndiceDisponibleType(DjangoObjectType):
    class Meta:
        model = IndiceDisponible


class UserNotasType(DjangoObjectType):
    class Meta:
        model = UserNotas


class HistoriaLineaType(DjangoObjectType):
    class Meta:
        model = HistoriaLinea


class DeviceType(DjangoObjectType):
    class Meta:
        model = UserDevice


class INEInfoType(DjangoObjectType):
    class Meta:
        model = INE_Info


class INERegAttemptType(DjangoObjectType):
    class Meta:
        model = INE_Reg_Attempt


class BeneficiarioType(DjangoObjectType):
    class Meta:
        model = UserBeneficiario


class ContactosType(DjangoObjectType):
    class Meta:
        model = Contacto


class ValidacionType(DjangoObjectType):
    class Meta:
        model = Telefono


class ComponentValidType(DjangoObjectType):
    class Meta:
        model = ComponentValidated


class ProfileComponentType(DjangoObjectType):
    class Meta:
        model = ProfileComponent


class IneRegValidationType(DjangoObjectType):
    class Meta:
        model = INE_Reg_Attempt


class CodigoConfianzaType(DjangoObjectType):
    class Meta:
        model = CodigoConfianza


class ParentescoType(DjangoObjectType):
    class Meta:
        model = Parentesco


class TransferenciasMensualesType(DjangoObjectType):
    class Meta:
        model = TransferenciasMensuales


class OperacionesMensualType(DjangoObjectType):
    class Meta:
        model = OperacionesMensual


class UsoCuentaType(DjangoObjectType):
    class Meta:
        model = UsoCuenta


class OrigenDepositoType(DjangoObjectType):
    class Meta:
        model = OrigenDeposito


class PerfilTransaccionalDeclaradoType(DjangoObjectType):
    class Meta:
        model = PerfilTransaccionalDeclarado


class AvatarType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    url = graphene.String()
    genero = graphene.String()
    activo = graphene.Boolean()


class ContactoInguzType(graphene.ObjectType):
    id = graphene.Int()
    alias = graphene.String()
    username = graphene.String()
    nombre = graphene.String()
    url = graphene.String()

    def resolve_alias(self, info):
        return self.Uprofile.alias

    def resolve_nombre(self, info):
        return self.get_full_name()

    def resolve_url(self, info):
        return self.Uprofile.avatar_url


class BuscadorInguzType(graphene.ObjectType):
    alias = graphene.String()
    nombre = graphene.String()
    apPaterno = graphene.String()
    apMaterno = graphene.String()
    clabe = graphene.String()
    url = graphene.String()
    agregado = graphene.Boolean()
    bloqueado = graphene.Int()

    def resolve_alias(self, info):
        return self.alias

    def resolve_nombre(self, info):
        return self.user.first_name

    def resolve_apPaterno(self, info):
        return self.user.last_name

    def resolve_apMaterno(self, info):
        return self.apMaterno

    def resolve_clabe(self, info):
        return self.cuentaClabe

    def resolve_url(self, info):
        return self.avatar_url

    def resolve_agregado(self, info):
        origen = info.context.user
        clabe = self.cuentaClabe
        try:
            print(self.user)
            contacto = origen.Contactos_Usuario.get(
                clabe=clabe,
                activo=True,
                bloqueado=False
            )
            return True
        except Exception as e:
            print(e)
            return False

    def resolve_bloqueado(self, info):
        origen = info.context.user
        clabe = self.cuentaClabe
        try:
            contacto = origen.Contactos_Usuario.get(
                clabe=clabe,
                activo=True,
                bloqueado=True
            )
            return contacto.id
        except Exception:
            return None


class BlockDetails(graphene.ObjectType):

    username = graphene.String()
    alias = graphene.String()
    clabe = graphene.String()
    time = graphene.types.datetime.DateTime()
    status = graphene.String()


class Query(graphene.ObjectType):
    """
        >>> Query (Pregunstas Secretas) Example:
            query{
            user(username: "fede", token: "eyJ0eXAiOiJ..."){
            preguntaseguridadSet{
            id
            pregunta
            respuestaseguridadSet{
                respuestaSecreta
            }
            }
        }
        }

        >>> Response:
        {
        "data": {
            "user": {
            "preguntaseguridadSet": [
                {
                "id": "1",
                "pregunta": "NOMBRE DE TU PRIMER MASCOTA",
                "respuestaseguridadSet": [
                    {
                    "respuestaSecreta": "DJ JC"
                    }
                ]
                },
                {
                "id": "2",
                "pregunta": "SEGUNDO NOMBRE DE TU PADRE/MADRE",
                "respuestaseguridadSet": [
                    {
                    "respuestaSecreta": "Jesus de Nazareth"
                    }
                ]
                }
            ]
            }
        }
        }
    """
    # QUERIES
    user = graphene.Field(TrueUserType,
                          user=graphene.Int(),
                          token=graphene.String(required=False),
                          username=graphene.String(),
                          description="`Query a single object from User \
                              Model:` using user(id) or username")

    all_users = graphene.List(TrueUserType,
                              description="`Query all the objects \
                                from the User Model`")

    user_profile = graphene.Field(UserProfileType,
                                  user_id=graphene.Int(required=False),
                                  token=graphene.String(required=False),
                                  description="`Query a single object from \
                                       UserProfile by its id`")
    all_user_profile = graphene.List(UserProfileType,
                                     description="`Query all the objects \
                                         from UserProfile Model`")

    beneficiario = graphene.List(BeneficiarioType,
                                 id=graphene.Int(),
                                 token=graphene.String(required=True),
                                 description="`Query a single object from the \
                                    beneficiarios model`")

    all_beneficiarios = graphene.List(BeneficiarioType,
                                      token=graphene.String(required=True),
                                      description="`Query all the objects \
                                    from the beneficiarios model`")

    status_registro = graphene.Field(StatusRegistroType,
                                     codigo=graphene.String(),
                                     descripcion=graphene.String(),
                                     description="`Query a single object \
                                         from StatusRegistro Model:` using \
                                         status_id(pk) or status")

    all_status_registro = graphene.List(StatusRegistroType,
                                        description="`Query all the objects \
                                            from the StatusRegistro Model`")

    status_cuenta = graphene.Field(StatusCuentaType,
                                   status_id=graphene.Int(),
                                   status=graphene.String(),
                                   description="`Query a single object from \
                                       the StatusCuenta model:` Using \
                                           pk(status_id) and status")

    all_status_cuenta = graphene.List(StatusCuentaType,
                                      description="`Query all the objects \
                                          from the StatusCuenta Model`")

    indice_disponible = graphene.Field(IndiceDisponibleType,
                                       indice_id=graphene.Int(),
                                       description="`Query a single object \
                                           from the IndiceDisponible Model`")

    all_indice_disponible = graphene.List(IndiceDisponibleType,
                                          description="`Query all the objects \
                                            from the IndiceDisponible Model`")

    user_nota = graphene.Field(UserNotasType,
                               user_nota_id=graphene.Int(),
                               description="`Query a single object from the \
                                   UserNota Model by its pk`")

    all_user_nota = graphene.List(UserNotasType,
                                  description="Query all the objects from the \
                                      UserNota model")

    historia_linea = graphene.Field(HistoriaLineaType,
                                    historia_linea_id=graphene.Int(),
                                    description="`Query a single object from the \
                                   HistoriaLinea Model by its pk`")

    all_historia_linea = graphene.List(HistoriaLineaType,
                                       description="`Query all the objects from the \
                                      HistoriaLinea model`")

    device = graphene.Field(DeviceType,
                            pk=graphene.Int(),
                            description="`Query a single object from Devices \
                              Model:` using pk")

    all_device = graphene.List(DeviceType,
                               description="Query all the objects from the \
                                           Device model")

    respuesta_secreta_seguridad = graphene.Field(RespuestaType,
                                                 id=graphene.Int(),
                                                 username=graphene.String(),
                                                 description="`Query a single object from the \
                                                 respuesta_secreta model`")

    all_respuesta_seguridad = graphene.List(RespuestaType,
                                            description="`Query all objects from the \
                                            respuesta_secreta model`")

    all_pregunta_seguridad = graphene.List(PreguntaType,
                                           tipo_nip=graphene.Boolean(),
                                           description="`Query all objects from the \
                                            pregunta_secreta model`")

    all_pregunta_seguridad_pwd = graphene.List(PreguntaType,
                                               description="`Query all objects from the \
                                            pregunta_secreta model`")

    all_contactos = graphene.List(ContactosType,
                                  limit=graphene.Int(),
                                  offset=graphene.Int(),
                                  ordering=graphene.String(),
                                  es_inguz=graphene.Boolean(),
                                  bloqueado=graphene.Boolean(),
                                  no_respaldos=graphene.Boolean(),
                                  activo=graphene.Boolean(),
                                  alias_inguz=graphene.String(),
                                  nombre=graphene.String(),
                                  token=graphene.String(required=True),
                                  description="`Query all the objects from the \
                                            lista contactos model`")
    get_INE_Profile = graphene.List(INERegAttemptType,
                                    token=graphene.String(required=True),
                                    description="`Query a single object from the \
                                    INE_Reg_Attempt model`")
    profile_valid = graphene.Field(ComponentValidType,
                                   token=graphene.String(required=True),
                                   c_key=graphene.String(required=True),
                                   description="Query the validity of a profile\
                                   component for a given user")
    profile_validities = graphene.List(ComponentValidType,
                                       token=graphene.String(required=True),
                                       description="Get the validities for all\
                                       profile components for user")
    user_respuestas = graphene.List(RespuestaType,
                                    token=graphene.String(required=True))

    user_preguntas = graphene.List(PreguntaType,
                                   token=graphene.String(required=True))

    all_parentesco = graphene.List(ParentescoType,
                                   description="Query all the objects from the\
                                   Parentesco Model")
    all_avatars = graphene.List(AvatarType,
                                description="Query all the objects from the\
                                Avatar Model")

    all_transferencias_mensuales = graphene.List(TransferenciasMensualesType,
                                                 description="Query all \
                                                 objects from the model \
                                                 Transferencias Mensuales")

    all_operaciones_mensuales = graphene.List(OperacionesMensualType,
                                              description="Query all objects \
                                              from the model \
                                              OperacionesMensual")

    all_uso_cuenta = graphene.List(UsoCuentaType,
                                   description="Query all objects from the \
                                   model UsoCuenta")

    all_origen_deposito = graphene.List(OrigenDepositoType,
                                        description="Query all objects from \
                                        model OrigenDeposito")

    # Initiating resolvers for type all Queries

    def resolve_all_avatars(self, info, **kwargs):
        """``allAvatars (Query): Query all the objects from Avatar Model``

            Arguments:
                - none

            Fields to query:
                - same from Avatar query.

            >>> Query Example:
            query{
            allAvatars {
                id
                name
                url
                }
            }
        """
        avatars = Avatar.objects.all()
        qs = []
        for avatar in avatars:
            dicc = {}
            dicc['id'] = avatar.id
            dicc['name'] = avatar.name
            dicc['genero'] = avatar.genero
            dicc['activo'] = avatar.activo
            try:
                dicc['url'] = str((avatar.avatar_img.url).split("?")[0])
            except Exception:
                dicc['url'] = "Objeto sin imagen"
            qs.append(dicc)
        return qs

    def resolve_all_user_profile(self, info, **kwargs):
        """``allUserProfile (Query): Query all the objects from UserProfile Model``

            Arguments:
                - none

            Fields to query:
                - same from userProfile query.

            >>> Query Example:
            query{
                allUsers{
                    id
                    username
                    firstName
                    email
                }
            }
        """
        return UserProfile.objects.all()

    def resolve_all_users(self, info, **kwargs):
        """
            ``all_users (Query): Query all objects from User Model``

            Arguments:
                - none

            Fields to query:
                - same from user query.

            >>> Query Example:
            query{
                allUsers{
                    id
                    username
                    firstName
                    email
                }
            }
            >>> Response:
            {
                "data": {
                    "allUsers": [
                        {
                            "id": "1",
                            "username": "javierpiedra",
                            "firstName": "Javier",
                            "email": "jpiedra@ppdc.mx"
                        },
                        {
                            "id": "2",
                            "username": "otroUsuario",
                            "firstName": "",
                            "email": ""
                        },
                        {
                            "id": "3",
                            "username": "aldo",
                            "firstName": "",
                            "email": "aldo@bratdev.com"
                        }
                    ]
                }
            }
        """
        return User.objects.all()

    def resolve_all_status_registro(self, info, **kwargs):
        """``allStatusRegistro (Query): Query all the objects from the \
                StatusRegistro Model``

                Arguments:
                    - none

                Fields to query:
                    - same from statusRegistro query.

            >>> Query Example:
            query{
                allStatusRegistro{
                    id
                    status
                    statusRegistro {
                        blockedDate
                        fechaNacimiento
                    }
                }
            }


            >>> Response:
            {
                "data": {
                    "allStatusRegistro": [
                        {
                            "id": "1",
                            "status": "TELEFONO REGISTRADO Y VALIDADO",
                            "statusRegistro": []
                        },
                        {
                            "id": "2",
                            "status": "INE Y COMPROBANTE DE DOMICILIO REGISTRADOS",
                            "statusRegistro": []
                        },
                        {
                            "id": "3",
                            "status": "PERFIL DE USUARIO COMPLETADO",
                            "statusRegistro": []
                        },
                        {
                            "id": "4",
                            "status": "NIP Y PREGUNTA SECRETA REGISTRADOS",
                            "statusRegistro": [
                                {
                                    "blockedDate": null,
                                    "fechaNacimiento": "1980-07-12"
                                }
                            ]
                        },
                        {
                            "id": "5",
                            "status": "CONTRATO DE APERTURA ACEPTADO",
                            "statusRegistro": [
                                {
                                    "blockedDate": null,
                                    "fechaNacimiento": "2019-08-13"
                                }
                            ]
                        },
                        {
                            "id": "6",
                            "status": "PRIMER DEPOSITO REALIZADO",
                            "statusRegistro": []
                        }
                    ]
                }
            }

        """
        return StatusRegistro.objects.all()

    def resolve_all_status_cuenta(self, info, **kwargs):
        """
            ``allStatusCuenta (Query): Query all the objects from the StatusCuenta \
            Model``

            Arguments:
                - None

            Fields to query:
                - same from the statusCuenta query

            >>> Query Example:
            query {
                allStatusCuenta{
                    id
                    status
                    statusCuenta {
                        blockedDate
                        fechaNacimiento
                    }
                }
            }

            >>> Response:
            {
                "data": {
                    "allStatusCuenta": [
                        {
                            "id": "1",
                            "status": "ACTIVO",
                            "statusCuenta": [
                                {
                                    "blockedDate": null,
                                    "fechaNacimiento": "2019-08-13"
                                },
                                {
                                    "blockedDate": null,
                                    "fechaNacimiento": "1980-07-12"
                                }
                            ]
                        },
                        {
                            "id": "2",
                            "status": "BLOQUEADO",
                            "statusCuenta": []
                        }
                    ]
                }
            }
        """
        return StatusCuenta.objects.all()

    def resolve_all_indice_disponible(self, info, **kwargs):
        """
            ``allIndiceDisponible (Query): Query all the objects from the \
                IndiceDisponible Model``

            Arguments:
                - None

            Fields to query:
                - Same from indiceDisponibleQuery

            >>> Query Example:
            query{
                allIndiceDisponible{
                    id
                    porcentaje
                    userprofileSet {
                        blockedDate
                        fechaNacimiento
                    }
                }
            }

            >>> Response:
            {
                "data": {
                    "allIndiceDisponible": [
                        {
                            "id": "1",
                            "porcentaje": 10,
                            "userprofileSet": [
                            {
                                "blockedDate": null,
                                "fechaNacimiento": "2019-08-13"
                            },
                            {
                                "blockedDate": null,
                                "fechaNacimiento": "1980-07-12"
                            }
                            ]
                        },
                        {
                            "id": "2",
                            "porcentaje": 20,
                            "userprofileSet": []
                        }
                    ]
                }
            }
        """
        return IndiceDisponible.objects.all()

    def resolve_all_user_nota(self, info, **kwargs):
        """``allUserNota (Query): Query all the objects from the UserNota model``

            Arguments:
                - None

            Fields to query:
                - Same from userNota query.

            >>> Query Example:
            query{
                allUserNota{
                    id
                    nota
                    fechaCreacion
                    user {
                        id
                    }
                    logger {
                        id
                    }
                }
            }

            >>> Response:
            {
                "data": {
                    "allUserNota": [
                    {
                        "id": "1",
                        "nota": "Una nota sobre el usuario",
                        "fechaCreacion": "2019-08-01T21:45:29+00:00",
                        "user": {
                            "id": "1"
                        },
                        "logger": {
                            "id": "2"
                        }
                    },
                    {
                        "id": "2",
                        "nota": "Otra nota de un usuario",
                        "fechaCreacion": "2019-08-01T21:47:28+00:00",
                        "user": {
                            "id": "2"
                        },
                        "logger": {
                            "id": "1"
                        }
                    }
                    ]
                }
            }
        """
        return UserNotas.objects.all()

    def resolve_all_historia_linea(self, info, **kwargs):
        """``allHistoriaLinea (Query): Query all objects from the \
            HistoriaLinea Model``

            Arguments:
                - None

            Fields to query:
                - Same from historiaLinea query

            >>> Query Example:
            query {
                allHistoriaLinea {
                    id
                    user {
                        id
                    }
                    lineaCredito
                    lineaDisponible
                    fechaApertura
                    fechaCierre
                    fechaCongelada
                    fechaUltTrans
                    saldoCuenta
                    fechaLinea
                    productos {
                        id
                    }
                    productos {
                        id
                    }
                }
            }
            >>> Response:
            {
                "data": {
                    "allHistoriaLinea": [
                        {
                        "id": "1",
                        "user": {
                            "id": "1"
                        },
                        "lineaCredito": 154225,
                        "lineaDisponible": 515151515,
                        "fechaApertura": "2019-08-22T19:49:56+00:00",
                        "fechaCierre": "2019-09-22T19:49:59+00:00",
                        "fechaCongelada": null,
                        "fechaUltTrans": null,
                        "saldoCuenta": 545,
                        "fechaLinea": "2019-08-22T19:49:19+00:00",
                        "productos": {
                            "id": "1"
                            }
                        }
                    ]
                }
            }
        """
        return HistoriaLinea.objects.all()

    @login_required
    def resolve_all_beneficiarios(self, info, **kwargs):
        user = info.context.user
        return user.User_Beneficiario.all()

    @login_required
    def resolve_all_respuesta_seguridad(self, info, **kwargs):
        return RespuestaSeguridad.objects.all()

    def resolve_all_pregunta_seguridad(self, info, tipo_nip=None, **kwargs):
        qs = PreguntaSeguridad.objects.all()
        if tipo_nip is not None:
            filter = Q(tipo_nip__exact=tipo_nip)
            qs = qs.filter(filter)
        return qs

    def resolve_all_pregunta_seguridad_pwd(self, info, **kwargs):
        return PreguntaSeguridad.objects.filter(tipo_nip=False)

    @login_required
    def resolve_user_respuestas(self, info, **kwargs):
        user = info.context.user
        if not user.is_anonymous:
            return RespuestaSeguridad.objects.filter(user=user)

    @login_required
    def resolve_user_preguntas(self, info, **kwargs):
        user = info.context.user
        if not user.is_anonymous:
            return PreguntaSeguridad.objects.filter(respuesta_secreta=user)

    @login_required
    def resolve_all_contactos(
            self, info, limit=None, offset=None, ordering=None, es_inguz=None,
            bloqueado=None, activo=None, alias_inguz=None,
            nombre=None, no_respaldos=None, **kwargs):

        user = info.context.user
        qs = user.Contactos_Usuario.all()

        if es_inguz:
            filter = (
                Q(es_inguz__exact=es_inguz)
            )
            qs = qs.filter(filter)
        elif es_inguz is False:
            filter = (
                Q(es_inguz__exact=es_inguz)
            )
            qs = qs.filter(filter)
        if bloqueado:
            filter = (
                Q(bloqueado__exact=bloqueado)
            )
            qs = qs.filter(filter)
        elif bloqueado is False:
            filter = (
                Q(bloqueado__exact=bloqueado)
            )
            qs = qs.filter(filter)
        if activo:
            filter = (
                Q(activo__exact=activo)
            )
            qs = qs.filter(filter)
        elif activo is False:
            filter = (
                Q(activo__exact=activo)
            )
            qs = qs.filter(filter)
        if alias_inguz:
            filter = (
                Q(alias_inguz__icontains=alias_inguz)
            )
            qs = qs.filter(filter)
        if no_respaldos:
            respaldos = Respaldo.objects.filter(
                Q(ordenante=user, activo=True) |
                Q(respaldo=user, activo=True)
            )
            for respaldo in respaldos:
                qs = qs.filter(filter).exclude(id=respaldo.contacto_id)
                if respaldo.respaldo == user:
                    u_clabe = respaldo.ordenante.Uprofile.cuentaClabe
                    qs = qs.filter(filter).exclude(clabe=u_clabe)

        if nombre:
            filter = (
                Q(nombre__icontains=nombre) |
                Q(ap_paterno__icontains=nombre) |
                Q(ap_materno__icontains=nombre) |
                Q(alias_inguz__icontains=nombre)
            )
            qs = qs.filter(filter)
        if ordering:
            qs = qs.order_by(ordering)
        if offset:
            qs = qs[offset:]
        if limit:
            qs = qs[:limit]
        for contacto in qs:
            if es_cuenta_inguz(contacto.clabe):
                try:
                    contacto_user = UserProfile.objects.get(
                        cuentaClabe=contacto.clabe,
                        status="O").user
                    contacto.alias_inguz = contacto_user.Uprofile.alias
                    if contacto_user.Uprofile.avatar:
                        contacto.avatar_url = (
                            contacto_user.Uprofile.avatar.avatar_img.url
                        ).split("?")[0]
                    else:
                        contacto.avatar_url = (Avatar.objects.get(
                            id=1).avatar_img.url).split("?")[0]
                except Exception:
                    contacto.activo = False
                    contacto.alias_inguz = "Cuenta inguz no encontrada"
                contacto.save()
        return (qs)

    @login_required
    def resolve_profile_validities(self, info, **kwargs):
        user = info.context.user
        validities = ComponentValidated.objects.filter(user=user)
        return validities

    # Initiating resolvers for type single Queries
    # p_total: participacion total de beneficiarios de un usuario, not returned
    @login_required
    def resolve_user_profile(self, info, **kwargs):
        """``userProfile (Query): Query a single object from UserProfile``

            Arguments:
                - userId (int): pk from the userProfile model object.

            Fields to query:
                - user
                - blockedReason
                - blockedDate
                - loginAttempts
                - loginAttemptsInside
                - status
                - apMaterno
                - sexo
                - curp
                - rfc
                - verificacionCurp
                - fechaNacimiento
                - verificacionEmail
                - statusRegistro
                - statusCuenta
                - autorizado
                - country
                - ine
                - ineReverso
                - comprobantedom
                - indiceDisponible
                - nip
                - statusNip
                - aceptaKitLegal

            >>> Query Example:
            query{
                userProfile(userId:1){
                    user {
                        id
                    }
                    blockedReason
                    blockedDate
                    loginAttempts
                    loginAttemptsInside
                    status
                    apMaterno
                    sexo
                    curp
                    rfc
                    verificacionCurp
                    fechaNacimiento
                    verificacionEmail
                    statusRegistro {
                        id
                    }
                    statusCuenta {
                        id
                    }
                    autorizado
                        country
                    ine {
                        id
                    }
                    ineReverso {
                        id
                    }
                    comprobantedom {
                        id
                    }
                    indiceDisponible {
                        id
                    }
                    nip
                    statusNip
                    aceptaKitLegal
                }
            }


            >>> Response:
            {
                "data": {
                    "userProfile": {
                    "user": {
                        "id": "1"
                    },
                    "blockedReason": "K",
                    "blockedDate": null,
                    "loginAttempts": 0,
                    "loginAttemptsInside": 0,
                    "status": "O",
                    "apMaterno": "Pérez",
                    "sexo": "M",
                    "curp": "AJSAH182837HDFDGV04",
                    "rfc": "AJSH837465EHU",
                    "verificacionCurp": true,
                    "fechaNacimiento": "2019-08-13",
                    "verificacionEmail": true,
                    "statusRegistro": {
                        "id": "5"
                    },
                    "statusCuenta": {
                        "id": "1"
                    },
                    "autorizado": true,
                    "country": "MX",
                    "ine": {
                        "id": "1"
                    },
                    "ineReverso": {
                        "id": "2"
                    },
                    "comprobantedom": {
                        "id": "3"
                    },
                    "indiceDisponible": {
                        "id": "1"
                    },
                    "nip": "",
                    "statusNip": "U",
                    "aceptaKitLegal": false
                    }
                }
            }
        """
        user = info.context.user
        if not user.is_anonymous:
            UP = UserProfile.objects.filter(user=user)
            if (len(UP) == 1):
                if UP[0].avatar:
                    url = UP[0].avatar.avatar_img.url
                    UP[0].avatar_url = url.split("?")[0]
                    UP[0].save()
                return UP[0]
            return None
        return None

    # @login_required
    def resolve_user(self, info, **kwargs):
        id_ = kwargs.get('user')
        username = kwargs.get('username')

        if id_ is not None:
            return User.objects.get(pk=id_)

        if username is not None:
            return User.objects.get(username=username)

        user = info.context.user
        if not user.is_anonymous:
            return user

        return None

    def resolve_status_registro(self, info, **kwargs):
        """``statusRegistro (Query): Query a single object from StatusRegistro Model``

                Arguments:
                    - status (string): A valid status in the model
                    - statusId (int): pk from the StatusRegistro Object

                Fields to query:
                    - id
                    - status
                    - statusRegistro

            >>> Query Example:
            query{
                statusRegistro(status:"NIP Y PREGUNTA SECRETA REGISTRADOS"){
                    id
                    status
                    statusRegistro {
                        blockedDate
                        fechaNacimiento
                    }
                }
            }


            >>> Response:
            {
                "data": {
                    "statusRegistro": {
                        "id": "4",
                        "status": "NIP Y PREGUNTA SECRETA REGISTRADOS",
                        "statusRegistro": [
                        {
                        "user": {
                            "id": "2"
                        },
                            "blockedDate": null,
                            "fechaNacimiento": "1980-07-12"
                        }
                    ]
                    }
                }
            }
        """
        id_ = kwargs.get('status_id')
        status = kwargs.get('status')

        if id_ is not None:
            return StatusRegistro.objects.get(pk=id_)

        if status is not None:
            return StatusRegistro.objects.get(status=status)

        return None

    def resolve_status_cuenta(self, info, **kwargs):
        """
            ``statusCuenta (Query): Query a single object from the StatusCuenta model``

            Arguments:
                - statusId (string): valid status from the StatusCuenta object.
                - status (int): pk from the StatusCuenta object.

            Fields to query:
                - id
                - status
                - statusCuenta

            >>> Query Example:
            query {
                statusCuenta(status: "ACTIVO") {
                    id
                    status
                    statusCuenta {
                        status
                        user {
                            id
                            username
                        }
                    }
                }
            }

            >>> Response:
            {
                "data": {
                    "statusCuenta": {
                        "id": "1",
                        "status": "ACTIVO",
                        "statusCuenta": [
                            {
                                "status": "O",
                                "user": {
                                    "id": "1",
                                    "username": "javierpiedra"
                            }
                            },
                            {
                                "status": "O",
                                "user": {
                                    "id": "2",
                                    "username": "otroUsuario"
                            }
                        }
                    ]
                    }
                }
            }
        """
        id_ = kwargs.get('status_id')
        status = kwargs.get('status')

        if id_ is not None:
            return StatusCuenta.objects.get(pk=id_)

        if status is not None:
            return StatusCuenta.objects.get(status=status)

        return None

    def resolve_indice_disponible(self, info, **kwargs):
        """
            ``indiceDisponible (Query): Query a single object from the \
                IndiceDisponible Model``

            Arguments:
                - indiceId: pk from the IndiceDisponible Model object

            Fields to query:
                - id
                - porcentaje
                - userprofileSet

            >>> Query Example:
            query{
                indiceDisponible(indiceId:1){
                    id
                    porcentaje
                    userprofileSet
                }
            }

            >>> Response:
            {
                "data": {
                    "indiceDisponible": {
                        "id": "1",
                        "porcentaje": 10,
                        "userprofileSet": [
                            {
                                "blockedDate": null,
                                "fechaNacimiento": "2019-08-13"
                            },
                            {
                                "blockedDate": null,
                                "fechaNacimiento": "1980-07-12"
                            }
                        ]
                    }
                }
            }
        """
        id_ = kwargs.get('indice_id')

        if id_ is not None:
            return IndiceDisponible.objects.get(pk=id_)

        return None

    def resolve_user_nota(self, info, **kwargs):
        """``userNota (Query): Query a single object from the UserNota Model by \
            its pk``

            Arguments:
                - userNotaId: pk from the UserNota Model object.

            Fields to query:
                - id
                - nota
                - fechaCreacion
                - user
                - logger

            >>> Query Example:
            query{
                userNota(userNotaId:1){
                    id
                    nota
                    fechaCreacion
                    user {
                        id
                    }
                    logger {
                        id
                    }
                }
            }

            >>> Response:
            {
                "data": {
                    "allIndiceDisponible": [
                        {
                            "id": "1",
                            "porcentaje": 10,
                            "userprofileSet": [
                            {
                                "blockedDate": null,
                                "fechaNacimiento": "2019-08-13"
                            },
                            {
                                "blockedDate": null,
                                "fechaNacimiento": "1980-07-12"
                            }
                            ]
                        },
                        {
                            "id": "2",
                            "porcentaje": 20,
                            "userprofileSet": []
                        }
                    ]
                }
            }
        """
        id_ = kwargs.get('user_nota_id')

        if id_ is not None:
            return UserNotas.objects.get(pk=id_)

        return None

    def resolve_historia_linea(self, info, **kwargs):
        """``historiaLinea (Query): Query a single object from the \
            HistoriaLinea Model``

            Arguments:
                - historiaLineaId: pk from the HistoriaLinea model object

            Fields to query:
                - id
                - user
                - lineaCredito
                - lineaDisponible
                - fechaApertura
                - fechaCierre
                - fechaCongelada
                - fechaUltTrans
                - saldoCuenta
                - fechaLinea
                - productos
                - productos

            >>> Query Example:
            query {
                historiaLinea(historiaLineaId: 1) {
                    id
                    user {
                        id
                    }
                    lineaCredito
                    lineaDisponible
                    fechaApertura
                    fechaCierre
                    fechaCongelada
                    fechaUltTrans
                    saldoCuenta
                    fechaLinea
                    productos {
                        id
                    }
                    productos {
                        id
                    }
                }
            }


            >>> Response:
            {
                "data": {
                    "historiaLinea": {
                    "id": "1",
                    "user": {
                        "id": "1"
                    },
                    "lineaCredito": 154225,
                    "lineaDisponible": 515151515,
                    "fechaApertura": "2019-08-22T19:49:56+00:00",
                    "fechaCierre": "2019-09-22T19:49:59+00:00",
                    "fechaCongelada": null,
                    "fechaUltTrans": null,
                    "saldoCuenta": 545,
                    "fechaLinea": "2019-08-22T19:49:19+00:00",
                    "productos": {
                        "id": "1"
                        }
                    }
                }
            }
        """
        id_ = kwargs.get('historia_linea_id')

        if id_ is not None:
            return HistoriaLinea.objects.get(pk=id_)

        return None

    def resolve_all_device(self, info, **kwargs):
        return UserDevice.objects.all()

    def resolve_device(self, info, **kwargs):
        id_ = kwargs.get('pk')

        if id_ is not None:
            return UserDevice.objects.get(pk=id_)

    def resolve_get_INE_Profile(self, info, **kwargs):
        user = info.context.user
        attempts = user.AttemptsSet.all()
        last_atttempt = len(attempts)-1
        attempts[last_atttempt].compare()
        attempts[last_atttempt].save()
        return attempts

    @login_required
    def resolve_beneficiario(self, info, **kwargs):
        user = info.context.user
        if not user.is_anonymous:
            beneficiario = user.User_Beneficiario.filter(activo=True)
            return beneficiario

    def resolve_respuesta_seguridad(self, info, **kwargs):
        id_ = kwargs.get('id')

        if id_ is not None:
            return RespuestaSeguridad.objects.get(pk=id_)
        return None

    @login_required
    def resolve_profile_valid(self, info, **kwargs):
        user = info.context.user
        component_id = kwargs.get('c_key')
        return ComponentValidated.objects.get(component=component_id,
                                              user=user)

    def resolve_all_parentesco(self, info, **kwargs):
        return Parentesco.objects.all()

    def resolve_all_transferencias_mensuales(self, info, **kwargs):
        return TransferenciasMensuales.objects.all()

    def resolve_all_operaciones_mensuales(self, info, **kwargs):
        return OperacionesMensual.objects.all()

    def resolve_all_uso_cuenta(self, info, **kwargs):
        return UsoCuenta.objects.all()

    def resolve_all_origen_deposito(self, info, **kwargs):
        return OrigenDeposito.objects.all()


class CreateUser(graphene.Mutation):
    """
        ``createUser (Mutation): Creates an user``

        Arguments:
            - password (string): At least 6 characters
            - username (string): User's phone number; eventually \
                this will fill the user's phone number field.

        Fields to query:
            - user: This will be the response we can get from this mutation.\
                The new instance of the recently created user.

        >>> Mutation Example:
        mutation{
            createUser(password:"x",username:"aa"){
                user{
                    id
                    username
                    dateJoined
                    }
                }
            }

        >>> Response:
        {
            "data": {
                "createUser": {
                    "user": {
                    "id": "7",
                    "username": "aa",
                    "dateJoined": "2019-08-20T22:42:57.325361+00:00"
                    }
                }
            }
        }

        >>> userTelefonos query Example:
        query{
            userTelefonos(user: 1){
            id
            telefono
            }
        }

        >>> Response:
            {
            "data": {
            "userTelefonos": [
            {
                "id": "1",
                "telefono": "5548754578"
            },
            {"id": "4",
            "telefono": "5585457584"}
                ]
            }
        }

        >>> PreguntaSeguridad query Example:
        query{
            userTelefonos(user: 1){
            id
            telefono
            }
        }
    """
    user = graphene.Field(TrueUserType)
    statusRegistro = graphene.Field(StatusRegistroType)
    codigoconfianza = graphene.Field(CodigoConfianzaType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String()
        codigo_referencia = graphene.String()
        test = graphene.Boolean()

    def mutate(self, info, username, codigo_referencia=None,
               password=None, test=False):
        uuid = info.context.headers.get("Device-Id")
        lat = info.context.headers.get("Location-Lat")
        lon = info.context.headers.get("Location-Lon")
        if not (lat and lon and uuid) and not test:
            raise Exception("Faltan headers en la petición")
        if test is not True:
            geolocator = Nominatim(user_agent="cactus")
            location = geolocator.reverse((lat, lon))
            if location.raw['address']['country_code'] != "mx":
                raise Exception("Usuario fuera de territorio Mexicano")
        try:
            user = User.objects.get(username=username)
            return Exception("Ya existe un usuario con ese número")
        except Exception:
            try:
                telefono = Telefono.objects.get(
                    telefono=username,
                    activo=True,
                    validado=True)
            except Exception:
                raise Exception("El teléfono no ha sido validado")
            if password is not None:
                if codigo_referencia is None:
                    codigoconfianza = None
                else:
                    codigo_referencia = codigo_referencia.strip()
                    try:
                        codigoconfianza = CodigoConfianza.objects.get(
                            codigo_referencia=codigo_referencia)
                    except CodigoConfianza.DoesNotExist:
                        raise ValueError("Codigo de referencia invalido")
                username = username.strip()
                user = User.objects.create(username=username)
                user.set_password(password)
                user.is_active = True
                user.save()
                UP = UserProfile.objects.get(user=user)
                stat = StatusRegistro.objects.get(pk=1)
                UP.statusRegistro = stat
                site = os.getenv("SITE", "local")
                if ((site == "test") | (site == "stage") | (site == "prod")):
                    UP.saldo_cuenta = 0  # Verificar ambientes de desarrollo
                UP.usuarioCodigoConfianza = codigoconfianza
                UP.save()
                if not test:
                    telefono.user = user
                    telefono.validado = True
                    telefono.activo = True
                    telefono.save()
                    geo = GeoLocation.objects.create(
                        lat=lat,
                        lon=lon,
                    )
                    device = GeoDevice.objects.create(
                        uuid=uuid,
                        username=username,
                    )
                    UserLocation.objects.create(
                        user=user,
                        location=geo,
                        device=device,
                        date=timezone.now()
                    )
                    register_device(user=user)
                return CreateUser(user=user, codigoconfianza=codigoconfianza)
            else:
                return CreateUser(user=None)


class ChangePassword(graphene.Mutation):
    """
        ``changePassword (Mutation): changes the current password``

        Arguments:
            - newPassword (string): At least 6 characters
            - oldPassword (string): At least 6 characters
            - token (string): a session token for the user

        Fields to query:
            - user: This will be the response we can get from this mutation.\
                The new instance of the recently created user.

        >>> Mutation Example:
        mutation{
            changePassword(newPassword:"x",oldPassword:"y",token:"blah"){
                user{
                    id
                    username
                    dateJoined
                    }
                }
            }

        >>> Response:
        {
            "data": {
                "changePassword": {
                    "user": {
                    "id": "7",
                    "username": "aa",
                    "dateJoined": "2019-08-20T22:42:57.325361+00:00"
                    }
                }
            }
        }
    """
    user = graphene.Field(TrueUserType)

    class Arguments:
        token = graphene.String(required=True)
        new_password = graphene.String(required=True)
        old_password = graphene.String(required=True)

    def mutate(self,
               info,
               token,
               new_password,
               old_password):
        user = info.context.user
        if not user.is_anonymous:
            if user.check_password(old_password):
                if user.check_password(new_password):
                    raise Exception("La nueva contraseña no puede "
                                    "ser igual a la anterior.")
                user.set_password(new_password)
                user.save()
                return ChangePassword(user=user)
            raise AssertionError("Contraseña actual incorrecta")


class DeleteDevice(graphene.Mutation):
    """
        ``DeleteDevice (Mutation): Deletes a device before or after an user``
        Arguments:
        - pk (int): Unique app id neccesary

        >>> Mutation Example:
        mutation{
        deleteDevice(pk:1){
            ok
        }
        }
        >>> Response:
        {
            "data": {
                "deleteDevice": {
                    "ok": true
                }
            }
        }
    """
    ok = graphene.Boolean()

    class Arguments:
        pk = graphene.Int(required=True)

    def mutate(self, info, pk):
        device = UserDevice.objects.get(pk=pk)
        device.active = False
        device.save()

        return DeleteDevice(ok=True)


class CreateDevice(graphene.Mutation):
    """
        ``CreateDevice (Mutation): Creates a device before or after an user``
        Arguments:
        - pk (int): Primary key
        - deviceOS (string) : possible OS of the device
        - deviceMAC: MAC
        - deviceGPS: Location
        - deviceActive: If the device is the ine that is active

        >>> Mutation Example:
        mutation{
        createDevice(pk:1){
            device{
                pk
                }
            }
        }
        >>> Response:
        {
        "data": {
            "createDevice": {
                "device": {
                    "pk": "ADSFADS88787ASDF"
                    }
                    }
    """
    device = graphene.Field(DeviceType)

    class Arguments:
        create = graphene.Boolean(required=True)
        pk = graphene.Int()
        os = graphene.String()
        mac = graphene.String()
        gps = graphene.String()
        active = graphene.Boolean()
        gps = graphene.String()
        unique_id = graphene.String()
        name = graphene.String()
        brand = graphene.String()
        dev_model = graphene.String()

    def mutate(self, info, create, pk=None, os=None, mac=None, gps=None,
               active=False, unique_id=None, name=None, dev_model=None,
               brand=None):

        user = info.context.user
        if (user.__str__() == "AnonymousUser"):
            user = None

        if not create:
            device = UserDevice.objects.get(pk=pk)
            device.os = os if os else device.os
            device.mac = mac if mac else device.mac
            device.gps = gps if gps else device.gps
            device.active = active if active else device.active
            device.unique_id = unique_id if unique_id else device.unique_id
            device.name = name if name else device.name
            device.dev_model = dev_model if dev_model else device.dev_model
            device.brand = brand if brand else device.brand
        else:
            if create and pk:
                raise ValueError("Cannot create with Primary key given")
            try:
                device = UserDevice.objects.get(unique_id=unique_id)
            except Exception:
                device = UserDevice.objects.create(user=user,
                                                   os=os,
                                                   mac=mac,
                                                   gps=gps,
                                                   active=active,
                                                   unique_id=unique_id,
                                                   brand=brand,
                                                   dev_model=dev_model,
                                                   name=name)

        device.save()
        return CreateDevice(device=device)


class RegisterIneFront(graphene.Mutation):
    user = graphene.Field(TrueUserType)

    class Arguments:
        token = graphene.String(required=True)
        first_name = graphene.String(required=True)
        apellido_paterno = graphene.String(required=True)
        apellido_materno = graphene.String(required=True)
        curp = graphene.String(required=True)
        numero_INE = graphene.String(required=True)

    def mutate(self,
               info,
               token,
               first_name=None,
               apellido_paterno=None,
               apellido_materno=None,
               curp=None,
               numero_INE=None):
        if first_name is not None:
            first_name = first_name.strip()
        if apellido_paterno is not None:
            apellido_paterno = apellido_paterno.strip()
        if apellido_materno is not None:
            apellido_materno = apellido_materno.strip()
        if curp is not None:
            curp = curp.strip()
        if numero_INE is not None:
            numero_INE = numero_INE.strip()
        user = info.context.user
        front = INE_Info.objects.create(user=user, firstName=first_name,
                                        apellido_paterno=apellido_paterno,
                                        apellido_materno=apellido_materno,
                                        curp=curp,
                                        numero_INE=numero_INE)
        INE_Reg_Attempt.objects.create(user=user, front=front)
        return RegisterIneFront(user=user)


class RegisterIneBack(graphene.Mutation):
    user = graphene.Field(TrueUserType)

    class Arguments:
        token = graphene.String(required=True)
        first_name = graphene.String(required=True)
        apellido_paterno = graphene.String(required=True)
        apellido_materno = graphene.String(required=True)
        curp = graphene.String(required=True)
        numero_INE = graphene.String(required=True)

    def mutate(self,
               info,
               token,
               first_name=None,
               apellido_paterno=None,
               apellido_materno=None,
               curp=None,
               numero_INE=None):
        if first_name is not None:
            first_name = first_name.strip()
        if apellido_paterno is not None:
            apellido_paterno = apellido_paterno.strip()
        if apellido_materno is not None:
            apellido_materno = apellido_materno.strip()
        if curp is not None:
            curp = curp.strip()
        if numero_INE is not None:
            numero_INE = numero_INE.strip()
        user = info.context.user
        back = INE_Info.objects.create(user=user, firstName=first_name,
                                       apellido_paterno=apellido_paterno,
                                       apellido_materno=apellido_materno,
                                       curp=curp,
                                       numero_INE=numero_INE)
        attempts = user.AttemptsSet.all()
        last_attempt = len(attempts)-1
        attempts[last_attempt].back = back
        attempts[last_attempt].save()
        # print(attempts[lastAttemp].compare())
        return RegisterIneBack(user=user)


class UpdateUser(graphene.Mutation):
    user = graphene.Field(TrueUserType)

    class Arguments:
        token = graphene.String(required=True)
        newname = graphene.String(required=True)

    def mutate(self, info, token, newname):
        user = info.context.user
        if not user.is_anonymous and newname:
            tel = user.user_telefono.filter(activo=True)
            for t in tel:
                t.activo = False
                t.save()
            newname = newname.strip()
            Telefono.objects.create(telefono=newname,
                                    user=user)

        return UpdateUser(user=user)


class UpdateInfoPersonal(graphene.Mutation):
    user = graphene.Field(TrueUserType)
    profile_valid = graphene.List(ComponentValidType)

    class Arguments:
        token = graphene.String(required=True)
        alias = graphene.String()
        name = graphene.String()
        gender = graphene.String()
        name = graphene.String()
        last_name_p = graphene.String()
        last_name_m = graphene.String()
        birth_date = graphene.Date()
        nationality = graphene.String()
        country = graphene.String()
        city = graphene.String()
        numero_INE = graphene.String()
        occupation = graphene.String()
        curp = graphene.String()
        rfc = graphene.String()
        correo = graphene.String()
        avatarId = graphene.Int()

    def mutate(
        self, info, token,
        alias=None,
        name=None,
        gender=None,
        last_name_p=None,
        last_name_m=None,
        birth_date=None,
        nationality=None,
        country=None,
        city=None,
        numero_INE=None,
        occupation=None,
        curp=None,
        rfc=None,
        correo=None,
        avatarId=None,
    ):
        if name is not None:
            name = name.strip()
        if alias is not None:
            alias = alias.strip()
        if gender is not None:
            gender = gender.strip()
        if last_name_p is not None:
            last_name_p = last_name_p.strip()
        if last_name_m is not None:
            last_name_m = last_name_m.strip()
        if nationality is not None:
            nationality = nationality.strip()
        if curp is not None:
            curp = curp.upper()
        user = info.context.user
        if user.is_anonymous:
            raise AssertionError('usuario no identificado')
        if not user.is_anonymous:
            user.first_name = name if name else user.first_name
            user.last_name = last_name_p if last_name_p else user.last_name
            user.email = correo if correo else user.email
            u_profile = UserProfile.objects.filter(user=user)[0]
            u_profile.sexo = gender if gender else u_profile.sexo
            u_profile.apMaterno = (
                last_name_m if last_name_m else u_profile.apMaterno)
            u_profile.fecha_nacimiento = (
                birth_date if birth_date else u_profile.fecha_nacimiento)
            u_profile.nacionalidad = (
                nationality if nationality else u_profile.nacionalidad)
            u_profile.ciudad_nacimiento = city
            u_profile.numero_INE = (
                numero_INE if numero_INE else u_profile.numero_INE)
            u_profile.ocupacion = (
                occupation if occupation else u_profile.ocupacion)
            u_profile.curp = curp if curp else u_profile.curp
            u_profile.pais_origen_otro = (
                country if country else u_profile.pais_origen_otro)
            alias = alias if alias else u_profile.alias
            if alias and alias != u_profile.alias:
                if UserProfile.objects.filter(alias__iexact=alias).count() == 0:
                    u_profile.alias = alias if alias else u_profile.alias
                else:
                    raise AssertionError(
                        "Este alias ya fue tomado por otro cliente, "
                        "intenta algo diferente"
                    )
            elif alias and alias == u_profile.alias:
                pass
            else:
                # Genero Alias temporal para no romper la app actual
                u_profile.alias = str(
                    user.first_name.split()[0]) + str(user.id)
                # raise AssertionError (
                #     "Debes de ingresar un Alias a tu perfil"
                # )
            if avatarId:
                try:
                    avatarObject = Avatar.objects.get(id=avatarId)
                    u_profile.avatar = avatarObject
                    u_profile.avatar_url = (
                        u_profile.avatar.avatar_img.url).split("?")[0]
                except Exception:
                    raise AssertionError("Imagen de perfil inválida")
            elif (not avatarId) and (not u_profile.avatar):
                avatarObject = Avatar.objects.get(id=1)
                u_profile.avatar = avatarObject
                u_profile.avatar_url = (
                    u_profile.avatar.avatar_img.url).split("?")[0]
            rfc_valida = rfc if rfc else u_profile.rfc
            if not u_profile.curp:
                pass
            elif (rfc_valida is None or rfc_valida == "null") \
                    and u_profile.curp:
                u_profile.rfc = u_profile.curp[:10]
            elif (u_profile.rfc) == u_profile.curp[:10]:
                pass
            elif u_profile.curp and (InfoValidator.RFCValidado(rfc_valida, user) == rfc_valida):
                u_profile.rfc = rfc_valida
            else:
                raise AssertionError("RFC no válido")
            u_profile.save()
            message = InfoValidator.setCheckpoint(user=user, concepto='IP')
            u_profile.verificacion_curp = True
            if message == "curp validado":
                u_profile.verificacion_curp = True
            u_profile.save()
            user.save()
            try:
                validities = ComponentValidated.objects.filter(user=user)
            except Exception as e:
                raise AssertionError('no se ha podido establecer checkpoint',
                                     e)
            print("first_name: ", user.first_name)
            print("last_name: ", user.last_name)

            try:
                if not u_profile.cuentaClabe:
                    u_profile.registra_cuenta(user.first_name, user.last_name)
            except Exception as ex:
                AssertionError('Error al registrar la cuenta clabe.',
                               ex)
        return UpdateInfoPersonal(user=user, profile_valid=validities)


class CreateBeneficiario(graphene.Mutation):
    """
        ``createBeneficiario (Mutation): Creates a beneficiario for a user``

        Arguments:
            - Name (string): Beneficiario's name
            - Relacion (string) : Family relation to user

        Fields to query:
            - beneficiario: This will be the response we can get from this '\
            'mutation. The new instance of the recently created user.

        >>> Mutation Example:
        mutation{
            createBeneficiario(name:"Juan",relacion:"Padre"){
                beneficiario{
                    id
                    user{
                    username
                    }
                    name
                    relacion
                    }
                }
            }

        >>> Response:
        {
            "data": {
                "createBeneficiario": {
                    "beneficiario": {
                    "id": "1",
                    "user": "LMH",
                    "name": "Juan",
                    "parentesco": "Padre"
                    }
                }
            }
        }
    """
    beneficiario = graphene.Field(BeneficiarioType)
    profile_valid = graphene.List(ComponentValidType)

    class Arguments:
        token = graphene.String(required=True)
        nip = graphene.String(required=True)
        name = graphene.String(required=True)
        apellidopat = graphene.String()
        apellidomat = graphene.String()
        parentesco = graphene.Int(required=True)
        fecha_nacimiento = graphene.Date()
        telefono = graphene.String()
        calle = graphene.String()
        numeroexterior = graphene.String()
        numerointerior = graphene.String()
        codigopostal = graphene.String()
        colonia = graphene.String()
        municipio = graphene.String()
        estado = graphene.String()

    @login_required
    def mutate(self,
               info,
               token,
               nip,
               name,
               apellidopat,
               apellidomat,
               parentesco,
               calle,
               numeroexterior,
               numerointerior,
               codigopostal,
               colonia,
               municipio,
               estado,
               fecha_nacimiento,
               telefono):
        user = info.context.user
        if not user.is_anonymous:

            def _valida(expr, msg):
                if expr:
                    raise Exception(msg)

            _valida(user.Uprofile.password is None,
                    'El usuario no ha establecido su NIP.')
            _valida(not user.Uprofile.check_password(nip),
                    'El NIP es incorrecto.')

            if name is not None:
                name = name.strip()
            parentesco = Parentesco.objects.get(pk=parentesco)
            defaults = dict(
                nombre=name,
                parentesco=parentesco,
                apellido_paterno=apellidopat,
                apellido_materno=apellidomat,
                user=user,
                participacion=100,
                fecha_nacimiento=fecha_nacimiento,
                direccion_L1=calle,
                dir_num_ext=numeroexterior,
                dir_num_int=numerointerior,
                dir_CP=codigopostal,
                dir_colonia=colonia,
                dir_municipio=municipio,
                dir_estado=estado,
                telefono=telefono
            )
            try:
                try:
                    bene, created = UserBeneficiario.objects.update_or_create(
                        user=user,
                        defaults=defaults,
                    )
                except UserBeneficiario.MultipleObjectsReturned:
                    last = UserBeneficiario.objects.last().id
                    UserBeneficiario.objects.filter(
                        user=user).exclude(user=last).delete()
                    bene, created = UserBeneficiario.objects.update_or_create(
                        user = user,
                        defaults=defaults,
                    )
            except Exception:
                raise Exception("Error al crear el beneficiario, revisa los " \
                    "datos ingresados.")
        return CreateBeneficiario(
            beneficiario=bene, profile_valid=None)


class UpdateBeneficiario(graphene.Mutation):
    """
        ``updateBeneficiario (Mutation): Updates a Beneficiario``

        Arguments:
            -

        Fields to query:
            -

        >>> Mutation Example:

        >>> Response:
    """
    beneficiario = graphene.Field(BeneficiarioType)
    validities = graphene.List(ComponentValidType)

    class Arguments:
        token = graphene.String(required=True)
        benef_id = graphene.Int(required=True)
        name = graphene.String()
        parent_id = graphene.Int()
        f_nacimiento = graphene.Date()
        participacion = graphene.Float()

    def mutate(
        self, info, token, benef_id, name=None, parent_id=None,
        f_nacimiento=None, participacion=None
    ):
        user = info.context.user
        if user.is_anonymous:
            raise AssertionError('bad token')
        try:
            beneficiario = user.User_Beneficiario.get(pk=benef_id)
        except Exception:
            raise ValueError('no se encontro dicho beneficiarion relacionado\
                            al usuario')
        try:
            parentesco = Parentesco.objects.get(pk=parent_id)
        except Exception:
            raise ValueError('no existe el parentesco')
        if name:
            beneficiario.nombre = name
        if parentesco:
            beneficiario.parentesco = parentesco
        if f_nacimiento:
            beneficiario.f_nacimiento = f_nacimiento
        if participacion:
            beneficiario.participacion = participacion
            beneficiario.save()
            try:
                InfoValidator.setCheckpoint(user=user, concepto='CBN',
                                            beneficiario=beneficiario)
            except Exception as e:
                raise ValueError('no se pudo establecer el checkpoint', e)
        beneficiario.save()
        validities = ComponentValidated.objects.filter(user=user)
        return UpdateBeneficiario(beneficiario=beneficiario,
                                  validities=validities)


class DeleteBeneficiario(graphene.Mutation):
    """
        ``deleteBeneficiario (Mutation): Deactivate Beneficiario``

        Arguments:
            -id (id of associated user)
            -name (name of beneficiario to deactivate)

        >>> Mutation Example:
            deleteBeneficiario
                (id:4, name:"Chispa")
                {
                beneficiario{
                id
                    }
                }
                }

        >>> Response: "allUsers":
            {
                "id": "4",
                "username": "LMH",
                "UserBeneficiario": {
                    "id": "3",
                    "nombre": "Chispa",
                    "activo": false,
                    "user": {
                    "id": "4"
                    },
            },self.blocked_date = timezone.now()
    """

    beneficiario = graphene.Field(BeneficiarioType)

    class Arguments:
        token = graphene.String(required=True)
        id = graphene.Int(required=True)
        name = graphene.String()

    def mutate(self, info, token, id, name=None):
        user = info.context.user
        if not user.is_anonymous:
            beneficiario = user.User_Beneficiario.get(pk=id).delete()
            # beneficiario.activo = False
            # beneficiario.save()

        return DeleteBeneficiario(beneficiario=beneficiario)


class TokenAuthPregunta(graphene.Mutation):

    token = graphene.String()
    pin = graphene.String()

    class Arguments:
        pregunta_id = graphene.Int(required=True)
        respuesta_secreta = graphene.String(required=True)
        username = graphene.String(required=True)

    def mutate(self, info, username, pregunta_id, respuesta_secreta):
        pregunta = PreguntaSeguridad.objects.get(pk=pregunta_id)
        try:
            user = User.objects.get(username=username)
        except Exception:
            raise Exception("Usuario inválido")
        try:
            RespuestaSeguridad.objects.get(
                user=user,
                pregunta=pregunta,
                respuesta_secreta=respuesta_secreta,
                tipo_nip=False)
        except Exception:
            raise Exception("Datos incorrectos")
        pin = randint(100000, 999999)
        RestorePassword.objects.filter(user=user).delete()
        RestorePassword.objects.create(user=user,
                                       passTemporal=pin,
                                       activo=True)
        return TokenAuthPregunta(token=get_token(user), pin=pin)


class TokenAuthPreguntaNip(graphene.Mutation):

    nip = graphene.String()

    class Arguments:
        token = graphene.String()
        pregunta_id = graphene.Int(required=True)
        respuesta_secreta = graphene.String(required=True)
        username = graphene.String()

    def mutate(self, info, pregunta_id, respuesta_secreta,
        username=None, token=None
    ):
        pregunta = PreguntaSeguridad.objects.get(pk=pregunta_id)
        if username:
            user = User.objects.get(username=username)
        else:
            user = info.context.user
        try:
            RespuestaSeguridad.objects.get(
                user=user,
                pregunta=pregunta,
                respuesta_secreta=respuesta_secreta,
                tipo_nip=True)
        except Exception:
            raise Exception("Datos incorrectos")

        up = UserProfile.objects.get(user=user)
        up.statusNip = 'U'
        up.save()
        user.user_nipTemp.all().update(activo=False)
        nip = NipTemporal.objects.create(user=user).nip_temp
        InfoValidator.setCheckpoint(user=user, concepto='NIP')
        stat = StatusRegistro.objects.get(pk=5)
        up.statusRegistro = stat
        up.save()

        return TokenAuthPreguntaNip(nip=nip)


class UnBlockAccount(graphene.Mutation):

    details = graphene.String()

    class Arguments:

        username = graphene.String(required=True)
        password = graphene.String(required=True)
        nip = graphene.String(required=True)

    def mutate(self, info, username, password, nip):
        try:
            user = User.objects.get(username=username)
        except Exception:
            user = False
        if not user or not user.check_password(password) or \
            not user.Uprofile.check_password(nip):
                raise Exception("Credenciales de acceso incorrectas")
        up = user.Uprofile
        up.blocked_reason = up.NOT_BLOCKED
        up.status = up.OK
        up.save()
        user.save()
        InfoValidator.setComponentValidated(
            'bloqueo', user, True, motivo='')

        return UnBlockAccount(details='account UN_blocked')


class RecoverPassword(graphene.Mutation):

    details = graphene.String()

    class Arguments:
        pin = graphene.String(required=True)
        new_password = graphene.String(required=True)
        token = graphene.String(required=True)

    def mutate(self, info, pin, new_password, token):
        user = info.context.user
        if not user.is_anonymous:
            try:
                pass_temporal = RestorePassword.objects.filter(
                    user=user,
                    activo=True)[0]
                if pass_temporal.validate(pin):
                    if user.check_password(new_password):
                        raise Exception("La nueva contraseña no puede " \
                            "ser igual a la anterior.")
                    user.set_password(new_password)
                    pass_temporal.activo = False
                    pass_temporal.save()
                    user.save()
                    return RecoverPassword(details='password recuperado')
                else:
                    return RecoverPassword(details='pin invalido')
            except IndexError:
                raise AssertionError('pin inválido')


class UpdateNip(graphene.Mutation):
    """
        ``updateNip (Mutation): Updates a Nip``

        Arguments:
            -

        Fields to query:
            -

        >>> Mutation Example:

        >>> Response:

    """
    user_profile = graphene.Field(UserProfileType)
    profile_valid = graphene.List(ComponentValidType)

    class Arguments:
        old_nip = graphene.String(required=True)
        new_nip = graphene.String(required=True)
        token = graphene.String(required=True)

    def mutate(
        self, info, old_nip, new_nip, token
    ):
        user = info.context.user
        if not user.is_anonymous:
            if old_nip == new_nip:
                raise ValueError('nuevo nip no debe coincidir con el viejo')
            UP = UserProfile.objects.get(user=user)
            if UP.statusNip == 'U':
                if len(new_nip) != 4:
                    raise ValueError('NIP debe contener 4 caracteres')
                elif not new_nip.isnumeric():
                    raise ValueError('NIP debe ser numérico')
                else:
                    try:
                        nip_temporal = user.user_nipTemp.filter(
                            activo=True).last().nip_temp
                    except Exception:
                        raise ValueError("NIP temporal no está activo")
                    if nip_temporal == old_nip:
                        UP.set_password(new_nip)
                        UP.statusNip = 'A'
                        UP.enrolamiento = True
                        create_pld_customer(user)
                        RegistrarMail(user)
                    else:
                        raise ValueError('nip no coincide con el temporal')
            elif (UP.statusNip == 'A'):
                if not UP.check_password(old_nip):
                    raise ValueError('Nip esta mal')
                else:
                    UP.set_password(new_nip)
                    UP.statusNip = 'A'
                    print('NIP cambió exitosamente')
            else:
                raise ValueError('nip bloqueado')
            UP.save()
            InfoValidator.setCheckpoint(user=user, concepto='NIP')
            stat = StatusRegistro.objects.get(pk=15)
            UP.statusRegistro = stat
            UP.save()
            validities = ComponentValidated.objects.filter(user=user)
            return UpdateNip(user_profile=UP, profile_valid=validities)


class CreateContacto(graphene.Mutation):
    """
        ``createContacto (Mutation): Creates a contact for a user``

        Arguments:
            - nombre (string): Contact's short name
            - ap_paterno (string): Contact's full name
            - ap_materno (string): Contact's full name
            - banco (string): Contact's blank
            - clabe (string): Contact's clabe

        Fields to query:
            - contacto: This will be the response we can get from this '\
            'mutation. The new instance of the recently created user.

        >>> Mutation Example:
mutation{
    createContacto(nombre:"San",apMaterno:"Cuerito", apPaterno:"Blando", 	banco:"Banco Azteca",clabe:"01445778993775432", token:"token"){
        contacto{
            id
            user{
            username
            }
            nombre
            nombreCompleto
                apPaterno
                apMaterno
            banco
            clabe
            }
        }
    }

        >>> Response:
        {
            "data": {
                "createContacto": {
                    "contacto": {
                    "id": "1",
                    "user": "fede",
                    "nombre": "San",
                    "nombre_Completo": "San Juan Dieguito",
                    "banco": "Banco Azteca",
                    "clabe": "014456789098765432"
                    }
                }
            }
        }
    """
    contacto = graphene.Field(ContactosType)
    all_contactos = graphene.List(ContactosType)

    class Arguments:
        token = graphene.String(required=True)
        nombre = graphene.String()
        nombreCompleto = graphene.String()
        ap_paterno = graphene.String()
        ap_materno = graphene.String()
        banco = graphene.String()
        clabe = graphene.String()
        nip = graphene.String(required=True)

    def mutate(self, info, token, nip, nombreCompleto='', nombre='', ap_paterno='',
               ap_materno='', banco='', clabe=''):

        def _valida(expr, msg):
            if expr:
                raise Exception(msg)

        user = info.context.user
        _valida(user.Uprofile.password is None,
                'El usuario no ha establecido su NIP.')
        _valida(not user.Uprofile.check_password(nip),
                'El NIP es incorrecto.')

        try:
            name_banco = InstitutionBanjico.objects.get(
                short_id=str(clabe[:3])).short_name
        except Exception:
            raise Exception(
                'CLABE inválida, no existe banco válido para esa CLABE')
        if Contacto.objects.filter(user=user,
                                   clabe=clabe,
                                   activo=True,
                                   bloqueado=False).count() > 0:
            raise Exception(
                "Ya tienes esta CLABE agregada en tus contactos")
        if Contacto.objects.filter(user=user,
                            clabe=clabe,
                            activo=True,
                            bloqueado=True).count() > 0:
            raise Exception(
                "Esta cuenta CLABE la tienes en un contacto bloqueado, " \
                "desbloquéalo desde el buscador con su alias.")

        if not user.is_anonymous:
            nombre = nombre.strip()
            ap_paterno = ap_paterno.strip()
            ap_materno = ap_materno.strip()
            clabe = clabe.strip()
            nombre_completo = str(nombre) + " " + str(
                ap_paterno) + " " + str(ap_materno)
            es_inguz = es_cuenta_inguz(clabe)
            if es_inguz:
                try:
                    UserProfile.objects.get(
                        cuentaClabe=clabe,
                        enrolamiento=True,
                        status="O")
                except Exception:
                    raise Exception("No existe usuario Inguz con esa CLABE")
            contacto = Contacto.objects.create(nombre=nombre,
                                               ap_paterno=ap_paterno,
                                               ap_materno=ap_materno,
                                               nombreCompleto=nombre_completo,
                                               banco=name_banco,
                                               clabe=clabe,
                                               user=user,
                                               es_inguz=es_inguz)
        return CreateContacto(
            contacto=contacto,
            all_contactos=user.Contactos_Usuario.all())


class VerifyAddContactos(graphene.Mutation):
    contactos = graphene.List(ContactosType)
    creados = graphene.List(ContactosType)
    disponibles = graphene.List(ContactoInguzType)

    class Arguments:
        agenda = graphene.List(graphene.String)
        token = graphene.String(required=True)
        nip = graphene.String()
        agregar = graphene.Boolean()

    @login_required
    def mutate(self, info, token, agenda, nip=None, agregar=False):

        def _valida(expr, msg):
            if expr:
                raise Exception(msg)

        user = info.context.user
        clabes_agenda = list(map(
            lambda contacto: contacto.clabe,
            user.Contactos_Usuario.exclude(activo="False").exclude(
                clabe='')))

        usuarios_inguz = User.objects.filter(
            username__in=agenda).filter(
                is_staff=False).exclude(
                    username=user.username).exclude(
                        Uprofile__cuentaClabe__in=clabes_agenda).exclude(
                            Uprofile__cuentaClabe__isnull=True).exclude(
                                Uprofile__cuentaClabe='').exclude(
                                    Uprofile__enrolamiento=False)
        if agregar:

            _valida(user.Uprofile.password is None,
                    'El usuario no ha establecido su NIP.')
            _valida(not user.Uprofile.check_password(nip),
                    'El NIP es incorrecto.')

            lista_creados = []
            for usuario_inguz in usuarios_inguz:
                clabe = usuario_inguz.Uprofile.cuentaClabe.strip()

                # Validamos para que no se duplique
                if Contacto.objects.filter(
                        user=user, clabe=clabe, activo=True).count() == 0:
                    try:
                        nombre = usuario_inguz.first_name.strip()
                        ap_paterno = usuario_inguz.last_name.strip()
                        ap_materno = usuario_inguz.Uprofile.apMaterno.strip()
                        nombre_completo = (
                            usuario_inguz.Uprofile.get_nombre_completo()
                        )
                        contacto = Contacto.objects.create(
                            nombre=nombre,
                            ap_paterno=ap_paterno,
                            ap_materno=ap_materno,
                            nombreCompleto=nombre_completo,
                            banco="STP",
                            clabe=clabe,
                            user=user,
                            es_inguz=True
                        )
                        if contacto:
                            lista_creados.append(contacto)
                    except Exception as ex:
                        print("ex: ", ex)
                        msg = "[VerifyAddContactos] Error al crear contacto {}"
                        msg = msg.format(ex)
                        db_logger.error(msg)
            return VerifyAddContactos(
                contactos=user.Contactos_Usuario.all(),
                creados=lista_creados)

        return VerifyAddContactos(
            contactos=user.Contactos_Usuario.all(),
            disponibles=usuarios_inguz,
            creados=[])


class BlockContacto(graphene.Mutation):

    contacto = graphene.Field(ContactosType)
    details = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        bloquear = graphene.Boolean(required=True)
        clabe = graphene.String(required=True)
        nip = graphene.String(required=True)

    def mutate(self, info, token, bloquear, clabe, nip):

        user = info.context.user
        up = user.Uprofile
        if up.check_password(nip):
            if Contacto.objects.filter(user=user,
                                       clabe=clabe,
                                       activo=True).count() > 0:
                contacto = Contacto.objects.filter(clabe=clabe).update(
                    bloqueado=True)
                contacto = Contacto.objects.filter(clabe=clabe).first()
                return BlockContacto(contacto=contacto, details='Contacto Bloqueado')
            else:
                usuario_inguz = UserProfile.objects.filter(cuentaClabe=clabe)
                if usuario_inguz.count() == 0:
                    raise AssertionError('No existe el usuario con esta clabe')
                usuario_inguz = usuario_inguz.first()
                es_inguz = es_cuenta_inguz(clabe)
                try:
                    nombre_banco = InstitutionBanjico.objects.get(
                        short_id=str(clabe[:3])).short_name
                except Exception as e:
                    raise AssertionError(
                        'CLABE invalida, no existe banco valido para esa CLABE:', e)
                try:
                    nombre = usuario_inguz.user.first_name.strip()
                    ap_paterno = usuario_inguz.user.last_name.strip()
                    ap_materno = usuario_inguz.apMaterno.strip()
                    nombre_completo = str(nombre) + " " + str(
                        ap_paterno) + " " + str(ap_materno)
                    contacto = Contacto.objects.create(
                        nombre=nombre,
                        ap_paterno=ap_paterno,
                        ap_materno=ap_materno,
                        nombreCompleto=nombre_completo,
                        banco=nombre_banco,
                        clabe=clabe,
                        user=user,
                        es_inguz=es_inguz,
                        bloqueado=True
                    )
                except Exception as ex:
                    print("ex: ", ex)
                    msg = "[BlockContacto] Error al crear contacto {}"
                    msg = msg.format(ex)
                    db_logger.error(msg)
                return BlockContacto(contacto=contacto, details='Contacto Bloqueado')
        else:
            raise AssertionError("NIP esta mal")


class UnBlockContacto(graphene.Mutation):

    contacto = graphene.Field(ContactosType)
    details = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        id = graphene.Int(required=True)
        agregar = graphene.Boolean()

    def mutate(self, info, token, id, agregar=None):

        user = info.context.user
        if not user.is_anonymous:
            contacto = user.Contactos_Usuario.get(pk=id)
            if agregar is True:
                contacto.bloqueado = False
                contacto.save()
            if agregar is False:
                contacto.bloqueado = False
                contacto.activo = False
                contacto.save()
            return UnBlockContacto(contacto=contacto,
                                   details='Contacto Desbloqueado')


class UpdateContacto(graphene.Mutation):
    """
        ``updateContactos (Mutation): Updates a Contacto``

        Arguments:
            -

        Fields to query:
            -

        >>> Mutation Example:

        >>> Response:

    """
    contacto = graphene.Field(ContactosType)
    all_contactos = graphene.List(ContactosType)

    class Arguments:
        id = graphene.Int(required=True)
        token = graphene.String(required=True)
        nombre = graphene.String()
        nombre_completo = graphene.String()
        ap_paterno = graphene.String()
        ap_materno = graphene.String()
        banco = graphene.String()
        clabe = graphene.String()

    def mutate(self, info, id, token, nombre=None, nombre_completo=None,
               ap_paterno=None, ap_materno=None, banco=None, clabe=None):
        associated_user = info.context.user
        if not associated_user.is_anonymous:
            contacto = associated_user.Contactos_Usuario.get(pk=id)
            if nombre:
                contacto.nombre = nombre
            if nombre_completo:
                contacto.nombre_Completo = nombre_completo
            if ap_paterno:
                contacto.ap_paterno = ap_paterno
            if ap_materno:
                contacto.ap_materno = ap_materno
            if banco:
                contacto.banco = banco
            if clabe:
                contacto.clabe = clabe

            contacto.save()
        return UpdateContacto(contacto=contacto,
                              all_contactos=associated_user.
                              Contactos_Usuario.all())


class DeleteContacto(graphene.Mutation):
    """
        ``deleteContacto (Mutation): Deactivate Contacto``
        Arguments:
            -id (id of associated user)
            -nombre_Completo (Full name of contacto to deactivate)
        >>> Mutation Example:
        mutation{
            deleteContacto
                (token:"eyJ0eXAi...", nombreCompleto:'\
                '"Baronesa Sally Waldorf Von Lichestein III")
                {
                contacto{
                id
                    }
                }
                }
        >>> Response: "allUsers": [
            {
                "id": "4",
                "username": "fede",
                "Contacto": {
                    "id": "3",
                    "nombre_Completo": "Baronesa Sally Waldorf Von Lichestein III",
                    "activo": false,
                    "user": {
                    "id": "4"
                    },
            }
            ]
    """

    contacto = graphene.Field(ContactosType)
    all_contactos = graphene.List(ContactosType)

    class Arguments:
        token = graphene.String(required=True)
        clabe = graphene.String(required=True)
        nip = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, clabe, nip):
        associated_user = info.context.user
        if not associated_user.is_anonymous:
            up = associated_user.Uprofile
            if up.check_password(nip):
                try:
                    contacto = associated_user.Contactos_Usuario.get(
                        clabe=clabe, activo=True)
                    contacto.activo = False
                    contacto.save()
                except ObjectDoesNotExist:
                    raise Exception("No existe contacto activo")
                except MultipleObjectsReturned:
                    associated_user.Contactos_Usuario.filter(
                        clabe=clabe).update(activo=False)
                    contacto = associated_user.Contactos_Usuario.filter(
                        clabe=clabe).last()
                if contacto.es_inguz:
                    try:
                        contacto_user = User.objects.get(
                            Uprofile__cuentaClabe=contacto.clabe)
                        Respaldo.objects.filter(
                            Q(
                                ordenante=associated_user,
                                respaldo=contacto_user
                            ) |
                            Q(
                                ordenante=contacto_user,
                                respaldo=associated_user
                            )
                        ).update(activo=False, status="D")
                    except Exception:
                        pass
            else:
                raise AssertionError("NIP esta mal")
        return DeleteContacto(contacto=contacto,
                              all_contactos=associated_user.
                              Contactos_Usuario.all())


class BuscadorUsuarioInguz(graphene.Mutation):
    resultado = graphene.List(BuscadorInguzType)

    class Arguments:
        token = graphene.String(required=True)
        alias = graphene.String(graphene.String)
        max_coincidencias = graphene.Int()

    @login_required
    def mutate(self, info, token, alias, max_coincidencias=10):
        if len(alias) < 3:
            return BuscadorUsuarioInguz([])
        query = UserProfile.objects.filter(
            alias__startswith=alias,
            enrolamiento=True).exclude(
                alias__exact=(info.context.user.Uprofile.alias)).exclude(
                    status="C").exclude(cuentaClabe="")
        if query.count() > max_coincidencias:
            query = query[:max_coincidencias]
        return BuscadorUsuarioInguz(query.order_by('alias'))


class CreateUpdatePregunta(graphene.Mutation):
    respuesta = graphene.Field(RespuestaType)
    pregunta = graphene.Field(PreguntaType)

    class Arguments:
        token = graphene.String(required=True)
        pregunta_id = graphene.Int(required=True)
        respuesta = graphene.String(required=True)

    def mutate(self, info, token, respuesta, pregunta_id):
        user = info.context.user
        if not user.is_anonymous:
            pregunta = PreguntaSeguridad.objects.get(pk=pregunta_id)
            respuestas_nip = RespuestaSeguridad.objects.filter(user=user,
                                                               tipo_nip=True)
            for r in respuestas_nip:
                r.pregunta.respuesta_secreta.remove(user)
            if not RespuestaSeguridad.objects.filter(user=user,
                                                     pregunta=pregunta,
                                                     tipo_nip=True):
                pregunta.respuesta_secreta.add(user, through_defaults={
                    'respuesta_secreta': respuesta, 'tipo_nip': True})
                InfoValidator.setCheckpoint(user=user, concepto='NIP')

            else:
                raise ValueError(
                    "Operacion Invalida: Pregunta repetida/Fuera de rango")
            pregunta.save()
        else:
            raise ValueError("Operacion Invalida: Sin usuario asociado.")
        respuesta = RespuestaSeguridad.objects.get(user=user,
                                                   pregunta=pregunta)
        return CreateUpdatePregunta(pregunta=pregunta, respuesta=respuesta)


class CreateUpdatePreguntaForUser(graphene.Mutation):
    """
        ``CreateUpdatePreguntaForUser (Mutation): Assings a secret question for a'\
        'user``

        Arguments:
            - token (string): User
            - pregunta_id (int): PK of the secret question
            - respuesta (string): Answer to said question
            - editPreguntaId (int): PK of the question to Update/Change from user

        Fields to query:
            - User: This will be the response we can get from this '\
            'mutation. The new instance of the recently created question.

        >>> Mutation Example (Create):
        mutation{
            CreateUpdatePreguntaForUser(preguntaId: 1, respuesta:"DJ JC", '\
            'token:"eyJ0eXAiOi..."){
                pregunta{
                    pregunta
                    ...
                }
            }
        }

        >>> Response (Create):
        {
        "data": {
            "CreateUpdatePreguntaForUser": {
            "pregunta": {
                "id": "1"
            }
            }
        }
        }

        >>> Mutation Example (Update):
        mutation{
            CreateUpdatePreguntaForUser(editPreguntaId: 2, preguntaId: 2,'\
            'respuesta:"Jesus", token:"eyJ0eXAiOi..."){
                pregunta{
                    pregunta
                    ...
                }
            }
        }
        >>> Response (Update):
        {
        "data": {
            "CreateUpdatePreguntaForUser": {
            "pregunta": {
                "id": "2"
            }
            }
        }
        }

        >>> Mutation Example (Change):
        mutation{
            CreateUpdatePreguntaForUser(editPreguntaId: 3, preguntaId: 2,'\
                respuesta: "Pedro", token:"eyJ0eXAiOi..."){
                pregunta{
                    pregunta
                    ...
                }
            }
        }
        >>> Response (Change):
        {
        "data": {
            "CreateUpdatePreguntaForUser": {
            "pregunta": {
                "id": "3"
            }
            }
        }
        }

        ***
        Special Condition: If editPreguntaId & preguntaId already exists and
        editPreguntaId != preguntaId this will lead to the DELETION of
        editPreguntaId without a change happening.
        ***
    """
    respuesta = graphene.Field(RespuestaType)
    pregunta = graphene.Field(PreguntaType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        pregunta_id = graphene.Int(required=True)
        respuesta = graphene.String(required=True)

    def mutate(self, info, username, password, respuesta, pregunta_id):
        request = HttpRequest()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            pregunta = PreguntaSeguridad.objects.get(pk=pregunta_id)
            respuestas = RespuestaSeguridad.objects.filter(user=user,
                                                           tipo_nip=False)
            for r in respuestas:
                r.pregunta.respuesta_secreta.remove(user)
            if not RespuestaSeguridad.objects.filter(user=user,
                                                     pregunta=pregunta,
                                                     tipo_nip=False):
                pregunta.respuesta_secreta.add(user, through_defaults={
                    'respuesta_secreta': respuesta, 'tipo_nip': False})
            else:
                raise ValueError(
                    "Operacion Invalida: Pregunta repetida/Fuera de rango")
            pregunta.save()
            r = RespuestaSeguridad.objects.filter(user=user, tipo_nip=False)[0]
        else:
            raise ValueError("Operacion Invalida: Sin usuario asociado.")
        return CreateUpdatePreguntaForUser(pregunta=pregunta, respuesta=r)


class GenerateNipTemp(graphene.Mutation):

    nipTemp = graphene.String()

    class Arguments:
        token = graphene.String(required=True)

    def mutate(self, info, token):

        user = info.context.user
        if not user.is_anonymous:
            try:
                user.user_nipTemp.all().update(activo=False)
                pin = NipTemporal.objects.create(user=user).nip_temp
            except Exception:
                pin = None

        return GenerateNipTemp(nipTemp=pin)


class AcceptKitLegal(graphene.Mutation):

    success = graphene.Boolean()

    class Arguments:
        token = graphene.String(required=True)
        pwd = graphene.String(required=True)

    def mutate(self, info, token, pwd):
        user = info.context.user
        if not user.is_anonymous:
            UP = UserProfile.objects.filter(user=user)[0]
            if user.check_password(pwd):
                try:
                    UP.aceptaKitLegal = datetime.date.today()
                    UP.save()
                except Exception:
                    return AcceptKitLegal(success=False)
            else:
                return AcceptKitLegal(success=False)
            return AcceptKitLegal(success=True)


class ReceiveOCR(graphene.Mutation):
    status = graphene.String()
    detalles = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        validacion = graphene.Float(required=True)
        dict_foto = graphene.String(required=True)
        detalles = graphene.String(required=True)
        tipo = graphene.String(required=True)

    def mutate(self, info, username, tipo, validacion,
               detalles, dict_foto):

        user = User.objects.get(username=username)
        tipo = DocAdjuntoTipo.objects.get(tipo=tipo)
        documento = DocAdjunto.objects.filter(user=user, tipo=tipo).last()

        try:
            json.loads(dict_foto)
            json.loads(detalles)
            errores = ''

        except Exception as e:
            errores = 'Error OCR {}'.format(e)
        extraccion, _ = DocExtraction.objects.get_or_create(
            documento=documento)
        extraccion.validacion = validacion
        extraccion.diccionario = dict_foto
        extraccion.detalles = detalles
        extraccion.errores = errores
        extraccion.save()

        uprof = user.Uprofile

        if validacion < 0.85:
            # Don't invalidate while OCR is ugly
            # InfoValidator.setComponentValidated('InfoPersonal', user,
            #                                     False, 'OCR')
            # InfoValidator.setComponentValidated('direccion', user,
            #                                     False, 'OCR')
            uprof.ocr_ok = False

        if validacion > 0.85:
            uprof.ocr_ok = True

        uprof.save()

        print(detalles)
        print(validacion)
        print(dict_foto)
        print(errores)
        return ReceiveOCR(status='received', detalles=detalles)


class BlockAccount(graphene.Mutation):

    details = graphene.String()
    dateBlocked = graphene.String()

    class Arguments:
        nip = graphene.String(required=True)
        token = graphene.String(required=True)

    def mutate(self, info, token, nip):
        user = info.context.user
        if not user.is_anonymous:
            up = user.Uprofile
            if up.check_password(nip):
                date_blocked = timezone.now()
                up.blocked_date = date_blocked
                up.blockedReason = up.BLOCKED
                user.Ufecha.bloqueo = date_blocked
                up.blocked_reason = up.BLOCKED
                up.status = up.BLOCKED
                up.save()
                user.Ufecha.save()
                user.save()
                InfoValidator.setComponentValidated(
                    'bloqueo', user, False, motivo='cuenta bloqueada')
                return BlockAccount(details='account blocked')
            else:
                raise AssertionError('invalid operation, Wrong Credentials')

class BlockAccountEmergency(graphene.Mutation):

    details = graphene.Field(BlockDetails)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        nip = graphene.String(required=True)

    def mutate(self, info, username, password, nip):

        e = "Usuario y/o contraseña incorrectos"

        try:
            user = User.objects.get(username=username)
        except Exception:
            raise Exception(e)
        if not user.check_password(password):
            raise Exception(e)
        up = user.Uprofile
        if not up.check_password(nip):
            raise Exception("El NIP es incorrecto")
        status = "Cuenta bloqueada"
        if up.status == 'O':
            date_blocked = timezone.now()
            up.blocked_date = date_blocked
            up.blockedReason = up.BLOCKED
            user.Ufecha.bloqueo = date_blocked
            up.blocked_reason = up.BLOCKED
            up.status = up.BLOCKED
            up.save()
            user.Ufecha.save()
            user.save()
            InfoValidator.setComponentValidated(
                'bloqueo', user, False, motivo=status)
        else:
            date_blocked = user.Ufecha.bloqueo
        return BlockAccountEmergency(
                details=BlockDetails(
                    username=user.username,
                    alias=up.get_nombre_completo(),
                    clabe=up.cuentaClabe,
                    time=date_blocked,
                    status=status
                )
        )


class GetRnScreen(graphene.Mutation):

    rn_screen = graphene.String()

    class Arguments:
        token = graphene.String()

    def mutate(self, info, token):
        user = info.context.user
        components = ProfileComponent.objects.all().order_by('indice')
        screens = '{}'.format(user.username)
        for component in components:
            table = ComponentValidated.objects.get(component=component,
                                                   user=user)
            if table.status != 'VA':
                screens += ' {}'.format(component.alias)
        return GetRnScreen(rn_screen=screens)


class UpdateDevice(graphene.Mutation):

    validacion = graphene.String()


    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        nip = graphene.String(required=True)

    def mutate(self, info,username, password, nip):

        e = "Usuario y/o contraseña incorrectos"

        try:
            user = User.objects.get(username=username)
        except Exception:
            raise Exception(e)
        if not user.check_password(password):
            raise Exception(e)
        if not user.Uprofile.check_password(nip):
            raise Exception("El NIP es incorrecto")
        try:
            register_device(user=user)
            return UpdateDevice(validacion='Validado')
        except Exception as ex:
            db_logger.error("No se pudo actualizar dispositivo del usuario" \
            f"{user}. Error: {ex}")
            raise Exception('No se pudo actualizar dispositivo')


class CancelacionCuenta(graphene.Mutation):

    confirmacion = graphene.String()
    folio = graphene.String()
    fecha = graphene.types.datetime.DateTime()
    url = graphene.String()


    class Arguments:
        token = graphene.String(required=True)
        nip = graphene.String(required=True)

    def mutate(self, info, token, nip):
        user = info.context.user
        if user.is_anonymous:
            return
        if user.Uprofile.password is None:
            raise Exception('La cuenta no tiene NIP establecido')
        if not user.Uprofile.check_password(nip):
            raise Exception('El NIP es incorrecto')
        if not user.Uprofile.saldo_cuenta == 0:
            raise Exception('El saldo de tu cuenta debe ser $0 para cancelar')
        user.is_active = False
        user.save()
        folio = randomString()
        url = settings.URL_IMAGEN
        fecha = timezone.now()
        # Pendiente de crear movimiento no transaccional
        return CancelacionCuenta(
            confirmacion='OK', folio=folio, fecha=fecha, url=url)


class BorrarPreguntaSeguridad(graphene.Mutation):
    deleted = graphene.Boolean()

    class Arguments:
        id_pregunta = graphene.Int(required=True)

    def mutate(self, info, id_pregunta):
        try:
            u = PreguntaSeguridad.objects.get(pk=id_pregunta)
            u.delete()
            return BorrarPreguntaSeguridad(deleted=True)
        except PreguntaSeguridad.DoesNotExist:
            raise AssertionError('PreguntaSeguridad con es id no existe')


class RegistroCodi(graphene.Mutation):

    details = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        keySource = graphene.String(required=True)
        aliasSms = graphene.String(required=True)
        dvSub = graphene.String(required=True)

    def mutate(self, info, token, keySource, aliasSms, dvSub):

        user = info.context.user
        up = UserProfile.objects.get(user=user)
        if not user.is_anonymous:
            up.keySource = keySource
            up.aliasSms = aliasSms
            up.dvSub = dvSub
            up.registro_completo = True
            up.save()
        else:
            return Exception('Wrong Credentials')
        return RegistroCodi(details='Ok')


class ValidaCodi(graphene.Mutation):

    details = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        cd = graphene.String(required=True)

    def mutate(self, info, token, cd):

        user = info.context.user
        up = UserProfile.objects.get(user=user)
        if not user.is_anonymous:
            up.cd = cd
            up.verificada = True
            up.save()
        else:
            return Exception('Wrong Credentials')
        return ValidaCodi(details='Validado')


class UrlAvatar(graphene.Mutation):
    """
    ``UrlAvatar (Mutation): Gets the signed url for the user image profile
      (avatar)``
    """
    url = graphene.String()

    class Arguments:
        token = graphene.String(required=True)

    @login_required
    def mutate(self, info, token):

        if settings.SITE not in ["stage", "local"]:
            raise Exception("No está permitido el borrado en este ambiente")

        user = info.context.user
        try:
            avatar_url = (user.Uprofile.avatar.avatar_img.url).split("?")[0]
        except Exception:
            avatar_url = "Sin avatar"

        return UrlAvatar(url=avatar_url)


class DeleteBluepixelUser(graphene.Mutation):
    borrado = graphene.String()

    class Arguments:
        username = graphene.String(required=True)

    def mutate(self, info, username):

        msg = f"[DeleteBluepixelUser] Petición recibida. User: {username}"
        db_logger.info(msg)

        if settings.SITE not in ["stage", "local"]:
            raise Exception("No está permitido el borrado en este ambiente")

        bp_usernames = [
            "5568161651",
            "5567907071",
            "5611670737",
            "2871313291",
            "2871628373",
            "5586999540",
            "2223644726",
            "2212299619",
            "5520783405",
            "2871095852",
            "2871218166",
            "7714209743"
        ]
        if username not in bp_usernames:
            msg_ex = f"No está permitido borrar al usuario {username}"
            msg = "[DeleteBluepixelUser] " + msg_ex
            db_logger.info(msg)
            raise Exception(
                f"Sólo tienes permitido borrar los siguientes: {bp_usernames}")

        user = User.objects.filter(username=username)
        if user.count() == 0:
            msg_ex = f"No existe el usuario {username}"
            msg = "[DeleteBluepixelUser] " + msg_ex
            db_logger.info(msg)
            raise Exception(msg_ex)

        user = user.first()
        user.delete()
        msg = f"[DeleteBluepixelUser] Usuario {username} borrado"
        db_logger.info(msg)

        return DeleteBluepixelUser(borrado=f"Usuario {username} borrado")


class UnblockBluePixelUser(graphene.Mutation):
    desbloqueado = graphene.String()

    class Arguments:
        username = graphene.String(required=True)

    def mutate(self, info, username):

        msg = f"[UnblockBluePixelUser] Petición recibida. User: {username}"
        db_logger.info(msg)

        if settings.SITE not in ["stage", "local"]:
            raise Exception("No está permitido el borrado en este ambiente")

        bp_usernames = [
            "5568161651",
            "5567907071",
            "5611670737",
            "2871313291",
            "2871628373",
            "5586999540",
            "2223644726",
            "2212299619",
            "5520783405",
            "2871095852",
            "2871218166",
            "7714209743"
        ]
        if username not in bp_usernames:
            msg_ex = f"No está permitido borrar al usuario {username}"
            msg = "[UnblockBluePixelUser] " + msg_ex
            db_logger.info(msg)
            raise Exception(
                f"Sólo tienes permitido desbloquear los siguientes: \
                {bp_usernames}")

        user = User.objects.filter(username=username)
        if user.count() == 0:
            msg_ex = f"No existe el usuario {username}"
            msg = "[UnblockBluePixelUser] " + msg_ex
            db_logger.info(msg)
            raise Exception(msg_ex)
        user_ = User.objects.get(username=username)
        up = user_.Uprofile
        up.login_attempts = 0
        up.blocked_reason = "K"
        up.status = "O"
        up.save()
        user_.save()
        AccessAttempt.objects.filter(username=username).delete()
        msg = f"[UnblockBluePixelUser] Usuario {username} desbloqueado"
        db_logger.info(msg)

        return UnblockBluePixelUser(
            desbloqueado=f"Usuario {username} desbloqueado")


class SetPerfilTransaccional(graphene.Mutation):

    perfil = graphene.Field(PerfilTransaccionalDeclaradoType)

    class Arguments:
        token = graphene.String(required=True)
        transferencias_id = graphene.Int(required=True)
        operaciones_id = graphene.Int(required=True)
        uso_id = graphene.Int(required=True)
        origen_id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, token, transferencias_id, operaciones_id,
        uso_id, origen_id
    ):
        user = info.context.user
        transferencias = TransferenciasMensuales.objects.get(
            pk=transferencias_id)
        operaciones = OperacionesMensual.objects.get(pk=operaciones_id)
        uso = UsoCuenta.objects.get(pk=uso_id)
        origen = OrigenDeposito.objects.get(pk=origen_id)

        pd = PerfilTransaccionalDeclarado

        defaults = dict(
            transferencias_mensuales=transferencias,
            operaciones_mensuales=operaciones,
            uso_cuenta=uso,
            origen=origen,
            status_perfil='Pendiente'
        )

        try:
            perfil_declarado, created = pd.objects.update_or_create(
                user=user,
                defaults=defaults
                )
        except Exception:
            raise Exception("Error al crear perfil")
        return SetPerfilTransaccional(perfil=perfil_declarado)

class UpdateEmail(graphene.Mutation):

    correo = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        email_actual = graphene.String(required=True)
        email_nuevo = graphene.String(required=True)
        nip = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, email_actual, email_nuevo, nip):

        def _valida(expr, msg):
            if expr:
                raise Exception(msg)

        user = info.context.user

        _valida(user.Uprofile.password is None,
                'El usuario no ha establecido su NIP.')
        _valida(not user.Uprofile.check_password(nip),
                'El NIP es incorrecto.')
        _valida(not user.email == email_actual,
                'El correo actual no coincide')
        try:
            validate_email(email_nuevo)
        except Exception:
            raise Exception("Ingrese un correo válido")

        user.email = email_nuevo.lower()
        user.save()
        return UpdateEmail(correo=user.email)


class Mutation(graphene.ObjectType):
    delete_pregunta_seguridad = BorrarPreguntaSeguridad.Field()
    create_user = CreateUser.Field()
    change_password = ChangePassword.Field()
    update_user = UpdateUser.Field()
    create_device = CreateDevice.Field()
    delete_device = DeleteDevice.Field()
    create_beneficiario = CreateBeneficiario.Field()
    update_beneficiario = UpdateBeneficiario.Field()
    delete_beneficiario = DeleteBeneficiario.Field()
    update_nip = UpdateNip.Field()
    update_info_personal = UpdateInfoPersonal.Field()
    create_contacto = CreateContacto.Field()
    update_contacto = UpdateContacto.Field()
    delete_contacto = DeleteContacto.Field()
    create_update_pregunta = CreateUpdatePregunta.Field()
    create_update_pregunta_for_user = CreateUpdatePreguntaForUser.Field()
    generate_nip_temp = GenerateNipTemp.Field()
    register_Ine_Front = RegisterIneFront.Field()
    register_Ine_Back = RegisterIneBack.Field()
    accept_kit_legal = AcceptKitLegal.Field()
    recover_password = RecoverPassword.Field()
    token_auth_pregunta = TokenAuthPregunta.Field()
    token_auth_pregunta_nip = TokenAuthPreguntaNip.Field()
    receive_ocr = ReceiveOCR.Field()
    block_account = BlockAccount.Field()
    get_rnscreen = GetRnScreen.Field()
    update_device = UpdateDevice.Field()
    un_block_account = UnBlockAccount.Field()
    cancelacion_cuenta = CancelacionCuenta.Field()
    registro_codi = RegistroCodi.Field()
    valida_codi = ValidaCodi.Field()
    url_avatar = UrlAvatar.Field()
    verify_add_contactos = VerifyAddContactos.Field()
    block_contacto = BlockContacto.Field()
    buscador_usuario_inguz = BuscadorUsuarioInguz.Field()
    unblock_contacto = UnBlockContacto.Field()
    delete_bluepixel_user = DeleteBluepixelUser.Field()
    unblock_bluepixel_user = UnblockBluePixelUser.Field()
    set_perfil_transaccional = SetPerfilTransaccional.Field()
    block_account_emergency = BlockAccountEmergency.Field()
    update_email = UpdateEmail.Field()
