import graphene
# from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from demograficos.models.telefono import (TipoTelefono,
                                          ProveedorTelefonico,
                                          Telefono,
                                          PhoneVerification)
from demograficos.models.profileChecks import InfoValidator
import logging

db_logger = logging.getLogger("db")


class TipoTelefonoType(DjangoObjectType):
    class Meta:
        model = TipoTelefono


class ProveedorTelefonicoType(DjangoObjectType):
    class Meta:
        model = ProveedorTelefonico


class TelefonoType(DjangoObjectType):
    class Meta:
        model = Telefono


class PhoneVerificationType(DjangoObjectType):
    class Meta:
        model = PhoneVerification


class Query(object):
    """
    ``tipoTelefono (Query): Query a single object from the \
    TipoTelefono Model``

    Arguments:
        - tipoTelefonoId(int): pk from the HistoriaLinea model object
        - tipo (string): A valid "tipo" of HistoriaLinea model

    Fields to query:
        - id
        - tipo
        - telefonoSet

    >>> Query Example:
    query{
        tipoTelefono(tipo: "Movil"){
            id
            tipo
            telefonoSet {
                id
                telefono
            }
        }
    }

    >>> Response:
    {
        "data": {
            "tipoTelefono": {
                "id": "1",
                "tipo": "Movil",
                "telefonoSet": [
                    {
                       "id": "1",
                        "telefono": "5545857787"
                    },
                    {
                        "id": "2",
                        "telefono": "5547854785"
                    },
                    {
                        "id": "3",
                        "telefono": "4421545255"
                    }
                ]
            }
        }
    }


    ``allTipoTelefono (Query): Query all objects from the \
    TipoTelefono Model``

        Arguments:
            - None

        Fields to query:
            - Same from tipoTelefono query

    >>> Query Example:
    query{
        allTipoTelefono {
            id
            tipo
            telefonoSet {
                id
                telefono
            }
        }
    }

    >>> Response:
    {
        "data": {
            "allTipoTelefono": [
            {
                "id": "1",
                "tipo": "Movil",
                "telefonoSet": [
                {
                    "id": "1",
                    "telefono": "5567038596"
                },
                {
                    "id": "2",
                    "telefono": "5541616516"
                },
                {
                    "id": "3",
                    "telefono": "4421545255"
                }
                ]
            },
            {
                "id": "2",
                "tipo": "Casa",
                "telefonoSet": [
                {
                    "id": "4",
                    "telefono": "8596857444"
                }
                ]
            },
            {
                "id": "3",
                "tipo": "Oficina",
                "telefonoSet": [
                {
                    "id": "5",
                    "telefono": "4421562584"
                }
                ]
            }
            ]
        }
    }


    ``proveedorTelefonico (Query): Query a single object from the \
    ProveedorTelefonico Model``

        Arguments:
            - proveedorId (int): Primary key of the ProveedorTelefonico \
            model object.
            - proveedor (string): Name of the Proveedor.

        Fields to query:
            - id
            - proveedor
            - country
            - telefonoSet

    >>> Query Example:
    query{
        proveedorTelefonico(proveedorId:1){
            id
            proveedor
            country
            telefonoSet {
                id
            }
        }
    }

    >>> Response:
    {
        "data": {
                "proveedorTelefonico": {
                "id": "1",
                "proveedor": "Telcel",
                "country": "MX",
                "telefonoSet": [
                    {
                        "id": "2"
                    }
                ]
            }
        }
    }


    ``allProveedorTelefonico (Query): Query all objects from the \
    ProveedorTelefonico Model``

        Arguments:
            - None

        Fields to query:
            - Same from proveedorTelefonico query

    >>> Query Example:
    query{
        allProveedorTelefonico{
            id
            proveedor
            country
        }
    }

    >>> Response:
    {
        "data": {
            "allProveedorTelefonico": [
            {
                "id": "1",
                "proveedor": "Telcel",
                "country": "MX"
            },
            {
                "id": "2",
                "proveedor": "Movistar",
                "country": "MX"
            },
            {
                "id": "3",
                "proveedor": "AT&T",
                "country": "MX"
            },
            {
                "id": "4",
                "proveedor": "VirginMobile",
                "country": "MX"
            },
            {
                "id": "5",
                "proveedor": "Telmex",
                "country": "MX"
            },
            {
                "id": "6",
                "proveedor": "Axtel",
                "country": "MX"
            }
            ]
        }
    }


    ``telefono (Query): Query a single object from Telefono Model``

        Arguments:
            - telefonoId (int): pk from the Telefono Model Object
            - telefono (string): phone number of user.

        Fields to query:
            - id
            - telefono
            - extension
            - fechaCreacion
            - country
            - prefijo
            - activo
            - validado
            - user
            - proveedorTelefonico
            - tipoTelefono

    >>> Query Example:
    query {
        telefono(telefonoId: 1) {
            id
            telefono
            extension
            fechaCreacion
            country
            prefijo
            activo
            validado
            user {
                id
            }
            proveedorTelefonico {
                id
            }
            tipoTelefono {
                id
            }
        }
    }


    >>> Response:
    {
        "data": {
            "telefono": {
                "id": "1",
                "telefono": "5548754578",
                "extension": "",
                "fechaCreacion": "2019-08-15T22:53:03+00:00",
                "country": "MX",
                "prefijo": "+521",
                "activo": false,
                "validado": false,
                "user": {
                    "id": "1"
                },
                "proveedorTelefonico": {
                    "id": "3"
                },
                "tipoTelefono": {
                    "id": "1"
                }
            }
        }
    }

    ``allTelefono (Query): Query all objects from Telefono Model``

        Arguments:
            - None

        Fields to query:
            - Same from telefono query

    >>> Query Example:
    query{
        allTelefono{
            id
            telefono
            fechaCreacion
        }
    }


    >>> Response:
    {
        "data": {
            "allTelefono": [
            {
                "id": "1",
                "telefono": "5548754578",
                "fechaCreacion": "2019-08-15T22:53:03+00:00"
            },
            {
                "id": "2",
                "telefono": "5547854785",
                "fechaCreacion": "2019-08-15T22:55:26+00:00"
            },
            {
                "id": "3",
                "telefono": "4421545255",
                "fechaCreacion": "2019-08-15T22:58:27+00:00"
            },
            {
                "id": "4",
                "telefono": "5585457584",
                "fechaCreacion": "2019-08-15T22:59:04+00:00"
            },
            {
                "id": "5",
                "telefono": "5512365478",
                "fechaCreacion": "2019-08-15T23:00:02+00:00"
            }
            ]
        }
    }

    """

    tipo_telefono = graphene.Field(TipoTelefonoType,
                                   tipo_telefono_id=graphene.Int(),
                                   tipo=graphene.String(),
                                   description="`Query a single object from \
                                    TipoTelefono Model:` using  \
                                    tipoTelefonoId(pk) or tipo (string)")
    all_tipo_telefono = graphene.List(TipoTelefonoType,
                                      description="`Query all objects \
                                          from TipoTelefono Model`")

    proveedor_telefonico = graphene.Field(ProveedorTelefonicoType,
                                          proveedor_id=graphene.Int(),
                                          proveedor=graphene.String(),
                                          description="`Query a single object \
                                            from ProveedorTelefonico Model:` \
                                            using proveedorId (pk) or  \
                                            proveedor (string)")
    all_proveedor_telefonico = graphene.List(ProveedorTelefonicoType,
                                             description="`Query all objects \
                                             from ProveedorTelefonico Model`")

    telefono = graphene.Field(TelefonoType,
                              telefono_id=graphene.Int(),
                              telefono=graphene.String(),
                              description="Query a single object from \
                                            Telefono Model:` using \
                                            telefonoId (pk) or telefono \
                                            (string)")
    all_telefono = graphene.List(TelefonoType,
                                 description="`Query all objects \
                                             from Telefono Model`")

    # Initiating resolver for type all queries
    def resolve_all_tipo_telefono(self, info, **kwargs):
        return TipoTelefono.objects.all()

    def resolve_all_proveedor_telefonico(self, info, **kwargs):
        return ProveedorTelefonico.objects.all()

    def resolve_all_telefono(self, info, **kwargs):
        return Telefono.objects.all()

    # Initiating resolvers for type single queries
    def resolve_tipo_telefono(self, info, **kwargs):
        id = kwargs.get('tipo_telefono_id')
        tipo = kwargs.get('tipo')

        if id is not None:
            return TipoTelefono.objects.get(pk=id)

        if tipo is not None:
            return TipoTelefono.objects.get(tipo=tipo)

        return None

    def resolve_proveedor_telefonico(self, info, **kwargs):
        id = kwargs.get('proveedor_id')
        proveedor = kwargs.get('proveedor')

        if id is not None:
            return ProveedorTelefonico.objects.get(pk=id)

        if proveedor is not None:
            return ProveedorTelefonico.objects.get(proveedor=proveedor)

        return None

    def resolve_telefono(self, info, **kwargs):
        id = kwargs.get('telefono_id')
        telefono = kwargs.get('telefono')
        user_id = kwargs.get('user_id')

        if id is not None:
            return Telefono.objects.get(pk=id)

        if telefono is not None:
            return Telefono.objects.get(telefono=telefono)

        if user_id is not None:
            return Telefono.objects.get(user=user_id)

        return None


class CreateTelefono(graphene.Mutation):
    """
    ``CreateTelefono (Mutation): Creates a Telefono``

    Arguments:
        - numero = graphene.String(required=True)
        - token = graphene.String(required=True)
        - extension = graphene.String()
        - paisTel = graphene.String()
        - prefijo = graphene.String()
        - proveedor = graphene.String()

    Fields to query:
        - telefono: This will be the response we can get from this mutation.\
            The new instance of the recently created telefono.

    >>> Mutation Example:
    mutation{
        createTelefono(numero:"5512121212", prefijo:"52",
        paisTel:"MX",proveedor:"Telmex", extension:"123", test:true ){
            telefono{
                telefono
                activo
                extension
                prefijo
                validado
                country
                user {
                    username
                    }
                }
            }
        }

    >>> Response:
    {
      "data": {
        "createTelefono": {
          "telefono": {
            "telefono": "5512121212",
            "activo": true,
            "extension": "123",
            "prefijo": "52",
            "validado": false,
            "country": "MX",
            "user": {
              "username": "ernesto"
            }
          }
        }
      }
    }
    """
    telefono = graphene.Field(TelefonoType)

    class Arguments:
        numero = graphene.String(required=True)
        token = graphene.String()
        extension = graphene.String()
        paisTel = graphene.String()
        prefijo = graphene.String()
        proveedor = graphene.String()

    def mutate(self, info, numero, token=None, extension=None, paisTel=None,
               prefijo=None, proveedor=None):

        try:
            user = info.context.user
            if not user.is_anonymous:
                try:
                    tel = Telefono.objects.filter(telefono=numero)[0]
                    if tel.user != user:
                        raise Exception(
                            'telefono esta ocupado por otro usuario')
                    tel.activo = True
                    tel.extension = extension
                    tel.prefijo = prefijo
                    tel.country = paisTel
                    tel.save()
                except Exception:
                    Telefono.objects.filter(user=user).update(activo=False)
                    tel = Telefono.objects.create(telefono=numero,
                                                  activo=True,
                                                  extension=extension,
                                                  prefijo=prefijo,
                                                  validado=False,
                                                  country=paisTel,
                                                  user=user)

                    if proveedor is not None:
                        try:
                            prov = ProveedorTelefonico.get(
                                    proveedor__iexact=proveedor)
                        except Exception:
                            prov = ProveedorTelefonico.objects.create(
                                    proveedor=proveedor)
                            if paisTel is not None:
                                prov.country = paisTel
                                prov.save()

                        tel.proveedorTelefonico = prov
                        tel.save()

        except Exception as ex:
            tel = None
            raise ex

        return CreateTelefono(telefono=tel)


class SendSmsPin(graphene.Mutation):

    resp = graphene.Boolean()

    class Arguments:
        telefono = graphene.String(required=True)
        registro_nuevo = graphene.Boolean()

    def mutate(self, info, telefono, registro_nuevo=False):
        if registro_nuevo:
            if User.objects.filter(username=telefono).count() > 0:
                raise Exception("Telefono ya registrado en una cuenta Inguz")
            Telefono.objects.filter(
                telefono=telefono,
                user=None).delete()
            tel = Telefono.objects.create(
                telefono=telefono,
                activo=False,
                validado=False,
            )
            tel.send_token()
            return SendSms(resp=True)

        else:
            try:
                user = User.objects.get(username=telefono)
                user = Telefono.objects.filter(
                    telefono=telefono, user=user).last().user
                try:
                    tel = Telefono.objects.filter(user=user, telefono=telefono)
                    if len(tel) < 1:
                        raise Exception("User has no telefono")
                    tel = tel.filter(activo=True)[0]

                except Exception as e:
                    return Exception(str(e) + "User has no telefono activo")

            except Exception as ex:
                raise Exception('numero de telefono no existe ' + str(ex))
            if user.is_active is False:
                raise Exception("Cuenta cancelada y/o bloqueada")
            tel.send_token()
            return SendSms(resp=True)


class SendSms(graphene.Mutation):
    """
    ``SendSms (Mutation): Sends an SMS for verification``

    Arguments:
        - token = graphene.String()

    Fields to query:
        - resp: Wether the SMS was sent

    >>> Mutation Example:
    mutation{
      sendSms{
        resp
      }
    }

    >>> Response:
    {
      "data": {
        "sendSms": {
          "resp": true
        }
      }
    }
    """
    resp = graphene.Boolean()

    class Arguments:
        token = graphene.String()

    def mutate(self, info, token=None):
        resp = False
        user = info.context.user
        if not user.is_anonymous:
            try:
                tel = Telefono.objects.filter(user=user)

                if len(tel) < 1:
                    raise Exception("User has no telefono")

                tel = tel.filter(activo=True)[0]
            except Exception:
                raise Exception("User has no telefono activo")
        else:
            raise Exception("User must be authed")

        tel.send_token()
        resp = True

        return SendSms(resp=resp)


class UpdateTelefono(graphene.Mutation):
    """
    ``UpdateTelefono (Mutation): Updates a Telefono``

    Arguments:
        -

    Fields to query:
        -

    >>> Mutation Example:


    >>> Response:


    """

    telefono = graphene.Field(TelefonoType)

    class Arguments:
        nuevo_numero = graphene.String(required=True)
        extension = graphene.String()
        prefijo = graphene.String()
        userTel = graphene.String()
        proveedor = graphene.Int()
        token = graphene.String(required=True)

    def mutate(
        self, info, token=None, nuevo_numero=None, extension=None,
            prefijo=None, userTel=None, proveedor=None):
        try:
            user = info.context.user
            if not user.is_anonymous:

                tel = Telefono.objects.get(telefono=nuevo_numero)
                Telefono.objects.filter(user=user).exclude(
                                            pk=tel.pk).update(activo=False)
                if userTel:
                    tel.telefono = userTel
                if extension:
                    tel.extension = extension
                if prefijo:
                    tel.prefijo = prefijo
                if proveedor:
                    try:
                        tel.proveedor = ProveedorTelefonico.objects.get(
                                                                pk=proveedor)
                        tel.proveedor.save()
                    except Exception.DoesNotExist:
                        raise Exception(
                            "proveedor con id {} , no existe".format(
                                                                    proveedor))
                tel.save()

        except Exception as ex:
            tel = None
            raise ex

        return UpdateTelefono(telefono=tel)


class ValidacionTelefono(graphene.Mutation):
    validacion = graphene.String()

    class Arguments:
        numero = graphene.String(required=True)
        pin = graphene.String(required=True)
        enrolamiento = graphene.Boolean()
        test = graphene.Boolean()
        register_device = graphene.Boolean()

    def mutate(self, info, pin, numero, test=False, register_device=True,
               enrolamiento=False):

        if enrolamiento:
            tel = Telefono.objects.filter(telefono=numero, activo=False,
                validado=False)
            if tel.count() == 0:
                raise Exception('Número no registrado')
            tel = tel.last()
            if not test and not tel.is_valid(pin):
                return ValidacionTelefono(validacion="Incorrecto")
        else:
            tel = Telefono.objects.filter(telefono=numero).exclude(
                    user=None)
            if tel.count() == 0:
                raise Exception('No existe usuario asociado al teléfono')
            tel = tel.last()
            if not test and not tel.is_valid(pin):
                return ValidacionTelefono(validacion="Incorrecto")
            try:
                user = tel.user
                InfoValidator.setCheckpoint(
                    user=user, concepto='TEL',
                    register=register_device
                )
                user.is_active = True
                user.save()
                tel.activo = True
                tel.validado = True
                tel.save()
            except Exception as e:
                db_logger.error(f"[ValidacionTelefono] Error: {e}")
                return ValidacionTelefono(validacion=str(e))

        return ValidacionTelefono(validacion="Validado")


class VerifyUserNip(graphene.Mutation):
    validado = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        pin = graphene.String(required=True)

    def mutate(self, info, token, pin):
        user = info.context.user
        if user.is_anonymous:
            return
        if not user.Uprofile.check_password(pin):
            raise Exception('pin esta mal')
        return VerifyUserNip(validado=True)


class Mutation(graphene.ObjectType):
    validacion_telefono = ValidacionTelefono.Field()
    create_telefono = CreateTelefono.Field()
    update_telefono = UpdateTelefono.Field()
    send_sms = SendSms.Field()
    send_sms_pin = SendSmsPin.Field()
    verify_user_nip = VerifyUserNip.Field()
