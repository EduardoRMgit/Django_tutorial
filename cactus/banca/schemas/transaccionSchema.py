import graphene

from datetime import datetime

from django.utils import timezone
from django.contrib.auth import get_user_model

from graphene_django.types import DjangoObjectType

from graphql_jwt.decorators import login_required

from banca.models.transaccion import (Transaccion,
                                      StatusTrans,
                                      TipoAnual,
                                      SaldoReservado)
from banca.models.catalogos import TipoTransaccion

from spei.models import StpTransaction
from spei.stpTools import randomString
from spei.stpTools import gen_referencia_numerica

from demograficos.models.userProfile import UserProfile
from demograficos.models import Contacto


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class TransaccionType(DjangoObjectType):
    class Meta:
        model = Transaccion


class StpTransaccionType(DjangoObjectType):
    class Meta:
        model = StpTransaction


class StatusTransType(DjangoObjectType):
    class Meta:
        model = StatusTrans


class TipoAnualType(DjangoObjectType):
    class Meta:
        model = TipoAnual


class Query(object):
    """
    ``transaccion (Query)``
        Arguments:
            -

        Fields to query:
            - id
            - nombreArchivo
            - depositoRef
            - fechaArchivo
            - fechaOperacion
            - fechaAutorizado
            - montoTotalPagos
            - numRegistros
            - institucion
            - user
            - transpagoAuthdetSet

        >>> Query Example:
        query{
            transaccion(id:1, token: ""){
                id
                stpEstado
                statusTrans
                institucionOrdenante
                institucionBeneficiaria
                institucionOrdenanteInt {
                  id
                }
                institucionBeneficiariaInt {
                  id
                }
                stpId
                verifListaNegra
                contacto {
                  id
                }
                balance
                ubicacion
                time
                referencia
                referenciaNumerica
                stpMsg
                nombre
                banco
                clabe
                concepto
                empresa
                folioOrigen
                causaDevolucion
                monto
                nombreBeneficiario
                cuentaBeneficiario
                tipoCuentaBeneficiario
            }
        }
    >>> Response:
    {
        "data": {
            "transaccion": {
            "id": "1",
            "stpEstado": "A_0",
            "statusTrans": "A_0",
            "institucionOrdenante": null,
            "institucionBeneficiaria": null,
            "institucionOrdenanteInt": null,
            "institucionBeneficiariaInt": null,
            "stpId": "-1",
            "verifListaNegra": "O",
            "contacto": {
                "id": "1"
                },
            "balance": "-",
            "ubicacion": "adfadsfdasf",
            "time": "2020-06-02T14:41:25.612000+00:00",
            "referencia": "1234526482254125",
            "referenciaNumerica": "4400001",
            "stpMsg": "no nos quiere stp",
            "nombre": "Lucia Fernanda Brativano",
            "banco": "BBVA",
            "clabe": "012190021300378625",
            "concepto": "Papeleria2",
            "empresa": "INVERCRATOS",
            "folioOrigen": "000001",
            "causaDevolucion": null,
            "monto": "6259.00",
            "nombreBeneficiario": "Alan Gomez",
            "cuentaBeneficiario": "012190021300378625",
            "tipoCuentaBeneficiario": "40"
            }
        }
    }


    ``allStpTransaccion (Query): Query all objects from stpTransaccion Model``

        Arguments:
            - id: identifier of individual object, Int
            - fecha: date of creation for objects
            - token: user's credentials

        Fields to query:
            -id
            -stpEstado
            -statusTrans
            -institucionOrdenante
            -institucionBeneficiaria
            -institucionOrdenanteInt {}
            -institucionBeneficiariaInt {}
            -transaccion {}
            -user {}
            -stpMsg
            -stpId
            -nombre
            -banco
            -clabe
            -concepto
            -contacto {}
            -referencia
            -estado
            -empresa
            -folioOrigen
            -causaDevolucion
            -monto
            -fechaOperacion
            -claveRastreo
            -nombreOrdenante
            -tipoCuentaOrdenante
            -cuentaOrdenante
            -rfcCurpOrdenante
            -nombreBeneficiario
            -tipoCuentaBeneficiario
            -rfcCurpBeneficiario
            -institucionBeneficiaria
            -institucionBeneficiariaInt

        >>> Query Example:
            query{
                allStpTransaccion(token: ""){
                    id
                    stpEstado
                    statusTrans
                    institucionOrdenante
                    institucionBeneficiaria
                    institucionOrdenanteInt {
                      name
                    }
                    institucionBeneficiariaInt {
                      name
                    }
                    transaccion {
                      user{username}
                    }
                    user {
                      firstName
                    }
                    stpMsg
                    stpId
                    nombre
                    banco
                    clabe
                    concepto
                    contacto {
                      nombre
                    }
                    referencia
                    estado
                    empresa
                    folioOrigen
                    causaDevolucion
                    monto
                    fechaOperacion
                    claveRastreo
                    nombreOrdenante
                    tipoCuentaOrdenante
                    cuentaOrdenante
                    rfcCurpOrdenante
                    nombreBeneficiario
                    tipoCuentaBeneficiario
                    rfcCurpBeneficiario
                    institucionBeneficiaria
                    institucionBeneficiariaInt {
                          id
                        }
                }
            }

    >>>> Response
    {
      "data": {
        "allStpTransaccion": [
          {
            "id": "8",
            "stpEstado": "A_0",
            "statusTrans": "A_0",
            "institucionOrdenante": null,
            "institucionBeneficiaria": null,
            "institucionOrdenanteInt": null,
            "institucionBeneficiariaInt": null,
            "transaccion": {
              "user": {
                "username": "LMH"
              }
            },
            "user": {
              "firstName": ""
            },
            "stpMsg": "no nos quiere stp",
            "stpId": "-1",
            "nombre": "",
            "banco": "BBVA",
            "clabe": "012190011300378625",
            "concepto": "prueba",
            "contacto": {
              "nombre": "Lalo"
            },
            "referencia": "1234",
            "estado": null,
            "empresa": "INVERCRATOS",
            "folioOrigen": "000001",
            "causaDevolucion": null,
            "monto": "60.00",
            "fechaOperacion": "2020-06-26T17:24:52+00:00",
            "claveRastreo": "jamidlvbvf",
            "nombreOrdenante": "",
            "tipoCuentaOrdenante": "40",
            "cuentaOrdenante": "",
            "rfcCurpOrdenante": "",
            "nombreBeneficiario": "lasador",
            "tipoCuentaBeneficiario": "40",
            "rfcCurpBeneficiario": null
          },
          {
            "id": "9",
            "stpEstado": "A_0",
            "statusTrans": "A_0",
            "institucionOrdenante": null,
            "institucionBeneficiaria": null,
            "institucionOrdenanteInt": null,
            "institucionBeneficiariaInt": null,
            "transaccion": {
              "user": {
                "username": "LMH"
              }
            },
            "user": {
              "firstName": ""
            },
            "stpMsg": "no nos quiere stp",
            "stpId": "-1",
            "nombre": "",
            "banco": "BBVA",
            "clabe": "698765432123456789",
            "concepto": "prueba2",
            "contacto": {
              "nombre": "Lalo"
            },
            "referencia": "34456",
            "estado": null,
            "empresa": "INVERCRATOS",
            "folioOrigen": "000001",
            "causaDevolucion": null,
            "monto": "100.00",
            "fechaOperacion": "2020-06-26T17:44:24+00:00",
            "claveRastreo": "mwerwxhojo",
            "nombreOrdenante": "",
            "tipoCuentaOrdenante": "40",
            "cuentaOrdenante": "",
            "rfcCurpOrdenante": "",
            "nombreBeneficiario": "Laszlo",
            "tipoCuentaBeneficiario": "40",
            "rfcCurpBeneficiario": null
          }
        ]
      }
    }

    """
    transaccion = graphene.Field(StpTransaccionType,
                                 id=graphene.Int(),
                                 token=graphene.String())
    all_transaccion = graphene.List(TransaccionType,
                                    token=graphene.String())
    stp_transaccion = graphene.Field(StpTransaccionType,
                                     id=graphene.Int(),
                                     token=graphene.String())
    all_stp_transaccion = graphene.List(StpTransaccionType,
                                        id=graphene.Int(),
                                        fecha=graphene.String(),
                                        token=graphene.String())

    @login_required
    def resolve_all_transaccion(self, info, **kwargs):
        user = info.context.user
        if not user.is_anonymous:
            return Transaccion.objects.filter(user=user)
        return None

    @login_required
    def resolve_all_stp_transaccion(self, info, **kwargs):
        user = info.context.user
        y = kwargs.get('fecha')

        if not user.is_anonymous:
            if y is not None:
                date = datetime.strptime(y, "%Y, %m, %d")
                return StpTransaction.objects.filter(
                    fechaOperacion__month=date.month, user=user)
            else:
                return StpTransaction.objects.filter(user=user)

        return None

    @login_required
    def resolve_transaccion(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return StpTransaction.objects.get(pk=id)

        return None

    @login_required
    def resolve_stp_transaccion(self, info, **kwargs):
        id = kwargs.get('id')

        user = info.context.user
        if not user.is_anonymous:
            if id is not None:
                return StpTransaction.objects.get(pk=id)

        return None


class CreateTransferenciaEnviada(graphene.Mutation):
    """
    ``CreateTransferenciaEnviada (Mutation): Creates a transaction for STP``
       Arguments:
       - abono = graphene.String()
       - contacto
       - concepto = graphene.String()
       - nip

    >>> Mutation Example:
    mutation{
      createTransferenciaEnviada(
        concepto: "prueba"
        abono: "60.0"
        nip: "55287"
        contacto: 1
      }
    }
    >>> Response:
    {
    "data": {
        "createTransferenciaEnviada": {
            "stpTransaccion": {
                 "id": "354",
                }
                }
    }
                """

    stp_transaccion = graphene.Field(StpTransaccionType)
    user = graphene.Field(UserType)

    class Arguments:
        token = graphene.String(required=True)
        contacto = graphene.Int(required=True)
        abono = graphene.String(required=True)
        concepto = graphene.String(required=True)
        nip = graphene.String(required=True)
    # 3

    @login_required
    def mutate(self, info, token, contacto, abono, concepto, nip):

        def _valida(expr, msg):
            if expr:
                raise Exception(msg)
        abono = abono.strip()
        concepto = concepto.strip()
        nip = nip.strip()
        user = info.context.user
        monto = float(abono)
        saldo_inicial_usuario = user.Uprofile.saldo_cuenta

        _valida(UserProfile.objects.filter(user=user).count() == 0,
                'Usuario sin perfil')
        _valida(user.Uprofile.password is None,
                'El usuario no ha establecido su NIP.')
        _valida(not user.Uprofile.check_password(nip),
                'El NIP es incorrecto.')
        _valida(monto <= 0,
                'Únicamente montos positivos.')
        _valida(saldo_inicial_usuario - monto < 0,
                'Saldo insuficiente.')

        try:
            contacto = Contacto.objects.get(pk=contacto)
        except Exception:
            raise Exception('Contacto inexistente.')

        fecha = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        nombre_usuario = user.get_full_name()
        monto_stp_trans = "{:.2f}".format(monto)
        reservado_stp_trans = round(monto, 2)
        banco = contacto.banco
        clabe = contacto.clabe
        concepto = concepto.split(' - ')[-1]  # ???
        clave_rastreo = randomString()
        referencia = clave_rastreo[:int(len(clave_rastreo)/2)]
        ubicacion = "00"
        empresa = "ZYGOO"  # "INVERCRATOS2"
        folio_origen = "000001"
        tipo_cuenta_beneficiario = "40"
        tipo_cuenta_ordenante = "40"
        balance = 1  # ???
        status = StatusTrans.objects.get(nombre="esperando respuesta")
        tipo = TipoTransaccion.objects.get(codigo=2)  # Transferencia Enviada
        rfc_beneficiario = None
        main_trans = Transaccion.objects.create(
            user=user,
            fechaValor=fecha,
            monto=monto,
            statusTrans=status,
            tipoTrans=tipo,
            concepto=concepto,
            claveRastreo=clave_rastreo
        )

        stp_reservado = SaldoReservado.objects.create(
            tipoTrans=tipo,
            status_saldo="reservado",
            saldo_reservado=reservado_stp_trans
        )

        stp_transaccion = StpTransaction.objects.create(
            user=user,
            nombre=nombre_usuario,
            monto=monto_stp_trans,
            banco=banco,
            clabe=clabe,
            concepto=concepto,
            referencia=referencia,
            ubicacion=ubicacion,
            empresa=empresa,
            folioOrigen=folio_origen,
            claveRastreo=clave_rastreo,
            nombreOrdenante=nombre_usuario,
            nombreBeneficiario=contacto.nombre,
            tipoCuentaBeneficiario=tipo_cuenta_beneficiario,
            tipoCuentaOrdenante=tipo_cuenta_ordenante,
            fechaOperacion=fecha,
            rfcCurpOrdenante=user.Uprofile.curp,
            cuentaOrdenante=user.Uprofile.cuentaClabe,
            rfcCurpBeneficiario=rfc_beneficiario,
            referenciaNumerica=referencia,
            conceptoPago=concepto,
            cuentaBeneficiario=clabe,
            balance=balance,
            contacto=contacto,
            saldoReservado=stp_reservado,
            transaccion=main_trans
        )

        stp_transaccion.referenciaNumerica = gen_referencia_numerica({
            'id': stp_transaccion.id,
            'tipoCuentaBeneficiario': stp_transaccion.tipoCuentaBeneficiario,
            'tipoCuentaOrdenante': stp_transaccion.tipoCuentaOrdenante
        })
        stp_transaccion.save()

        valida = stp_transaccion.pago()
        if valida > 0:
            user.Uprofile.saldo_cuenta = round(
                float(saldo_inicial_usuario) - float(reservado_stp_trans), 2)
            user.Uprofile.save()
        print("\n\ntransacción creada:")
        for k in stp_transaccion.__dict__:
            print(f"    {k}:   {stp_transaccion.__dict__[k]}")

        return CreateTransferenciaEnviada(
            stp_transaccion=stp_transaccion,
            user=user
        )


# 4
class Mutation(graphene.ObjectType):
    create_transferencia_enviada = CreateTransferenciaEnviada.Field()
