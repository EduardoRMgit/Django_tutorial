import graphene

from datetime import datetime

from django.contrib.auth import get_user_model

from graphene_django.types import DjangoObjectType

from django.db.models import Q

from graphql_jwt.decorators import login_required

from banca.models.transaccion import (Transaccion,
                                      StatusTrans,
                                      TipoAnual,
                                      SaldoReservado)
from banca.models.catalogos import TipoTransaccion
from banca.models import (NotificacionCobro, InguzTransaction, NivelCuenta)
from banca.utils.clabe import es_cuenta_inguz
from banca.utils.limiteTrans import LimiteTrans
from banca.utils.comprobantesPng import CompTrans

from spei.models import StpTransaction
from spei.stpTools import randomString
from spei.stpTools import gen_referencia_numerica

from demograficos.models.userProfile import UserProfile
from demograficos.models import Contacto
from django.conf import settings
from banca.utils.cobroComision import comisionSTP


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class TransaccionType(DjangoObjectType):
    class Meta:
        model = Transaccion


class StpTransaccionType(DjangoObjectType):
    class Meta:
        model = StpTransaction
    comision = graphene.Float()

    def resolve_comision(self, info):
        if self.transaccion.comision:
            comision = 7.52
        else:
            comision = 0
        return comision


class StatusTransType(DjangoObjectType):
    class Meta:
        model = StatusTrans


class TipoAnualType(DjangoObjectType):
    class Meta:
        model = TipoAnual


class NotificacionCobroType(DjangoObjectType):
    class Meta:
        model = NotificacionCobro


class TipoTransType(DjangoObjectType):
    class Meta:
        model = TipoTransaccion


class NivelCuentaType(DjangoObjectType):

    class Meta:
        model = NivelCuenta

    nivel = graphene.Int()

    def resolve_nivel(self, info):
        return int(self.nivel)


class Query(graphene.ObjectType):
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
    transaccion = graphene.Field(TransaccionType,
                                 id=graphene.Int(),
                                 token=graphene.String())
    all_transaccion = graphene.List(TransaccionType,
                                    limit=graphene.Int(),
                                    offset=graphene.Int(),
                                    ordering=graphene.String(),
                                    token=graphene.String(required=True))
    stp_transaccion = graphene.Field(StpTransaccionType,
                                     id=graphene.Int(),
                                     token=graphene.String(required=True))
    all_stp_transaccion = graphene.List(StpTransaccionType,
                                        id=graphene.Int(),
                                        fecha=graphene.String(),
                                        token=graphene.String())
    all_cobros = graphene.List(NotificacionCobroType,
                               id=graphene.Int(),
                               status=graphene.String(),
                               limit=graphene.Int(),
                               offset=graphene.Int(),
                               ordering=graphene.String(),
                               token=graphene.String())

    all_nivel = graphene.List(NivelCuentaType)

    @login_required
    def resolve_all_transaccion(
        self, info, limit=None, offset=None, ordering=None, status=None,
        **kwargs
    ):
        user = info.context.user
        qs = user.user_transaccion.all()

        if ordering:
            qs = qs.order_by(ordering)
        if offset:
            qs = qs[offset:]
        if limit:
            qs = qs[:limit]

        return qs

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

    @login_required
    def resolve_all_cobros(
        self, info, limit=None, offset=None,
            ordering=None, id=None, status=None, **kwargs):
        user = info.context.user
        qs = user.mis_notificaciones_cobro.all()

        if id:
            filter = Q(id__iexact=id)
            qs = qs.filter(filter)
        if status:
            filter = Q(status__exact=status)
            qs = qs.filter(filter)
        if ordering:
            qs = qs.order_by(ordering)
        if offset:
            qs = qs[offset:]
        if limit:
            qs = qs[:limit]
        if not user.is_anonymous:
            for cobro in qs:
                cobro.valida_vencido()
                contacto_solicitante = Contacto.objects.filter(
                    user=user).filter(
                        clabe=cobro.usuario_solicitante.Uprofile.cuentaClabe)
                if contacto_solicitante.count() > 0:
                    _id = contacto_solicitante.first().pk
                    cobro.id_contacto_solicitante = _id
                else:
                    # El solicitante no existe en los contactos del deudor
                    cobro.id_contacto_solicitante = -1
                cobro.save()
        return qs

    def resolve_all_nivel(self, info):
        return NivelCuenta.objects.all()


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
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        nombre_usuario = user.get_full_name()
        monto_stp_trans = "{:.2f}".format(monto)
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
        if not LimiteTrans(user.id).trans_mes(float(monto_stp_trans)):
            raise Exception("Límite transaccional superado")
        main_trans = Transaccion.objects.create(
            user=user,
            fechaValor=fecha,
            monto=monto,
            statusTrans=status,
            tipoTrans=tipo,
            concepto=concepto,
            claveRastreo=clave_rastreo
        )
        comision, comision_m = comisionSTP(main_trans)
        comision = round(comision, 2)
        reservado_stp_trans = comision
        if comision_m:
            main_trans.comision = comision_m
            main_trans.comision.save()

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
        for k in stp_transaccion.__dict__:
            print(f"    {k}:   {stp_transaccion.__dict__[k]}")

        return CreateTransferenciaEnviada(
            stp_transaccion=stp_transaccion,
            user=user
        )


class CreateNotificacionCobro(graphene.Mutation):
    notificacion_cobro = graphene.Field(NotificacionCobroType)

    class Arguments:
        token = graphene.String(required=True)
        contacto_id = graphene.Int(required=True)
        importe = graphene.String(required=True)
        concepto = graphene.String(required=True)
        nip = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, contacto_id, importe, concepto, nip):
        def _valida(expr, msg):
            if expr:
                raise Exception(msg)

        user = info.context.user
        contacto = Contacto.objects.filter(pk=contacto_id)

        _valida(user.Uprofile.password is None,
                'El usuario no ha establecido su NIP.')
        _valida(not user.Uprofile.check_password(nip),
                'El NIP es incorrecto.')
        _valida(contacto.count() == 0,
                'Contacto inexistente.')
        contacto = contacto.first()
        _valida(contacto.user != user,
                'El contacto no pertenece al usuario.')

        _valida(float(importe) <= 0,
                'El monto del cobro debe ser positivo.')

        usuario_contacto = get_user_model().objects.filter(
            Uprofile__cuentaClabe=contacto.clabe)
        _valida(usuario_contacto.count() == 0,
                'No existe un usuario correspondiente al contacto.')

        usuario_contacto = usuario_contacto.first()
        qs = Contacto.objects.filter(
            user=usuario_contacto,
            clabe=user.Uprofile.cuentaClabe,
            bloqueado=True,
            activo=True
        )

        _valida(qs, "CB_NP")

        cobro = NotificacionCobro.objects.create(
            usuario_solicitante=user,
            usuario_deudor=usuario_contacto,
            importe=importe,
            concepto=concepto,
            clave_rastreo=randomString()
        )
        return CreateNotificacionCobro(
            notificacion_cobro=cobro
        )


class DeclinarCobro(graphene.Mutation):
    notificacion_cobro = graphene.Field(NotificacionCobroType)
    user = graphene.Field(UserType)

    class Arguments:
        token = graphene.String(required=True)
        cobro_id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, token, cobro_id):
        def _valida(expr, msg):
            if expr:
                raise Exception(msg)

        cobro = NotificacionCobro.objects.filter(pk=cobro_id)
        _valida(cobro.count() == 0,
                'Cobro inexistente.')

        cobro = cobro.first()
        cobro.valida_vencido()

        _valida(cobro.status == NotificacionCobro.VENCIDO,
                'El cobro está vencido.')
        _valida(cobro.status == NotificacionCobro.LIQUIDADO,
                'El cobro ya fue liquidado previamente.')
        _valida(cobro.status == NotificacionCobro.DECLINADO,
                'El cobro ya fue declinado proviamente.')
        cobro.status = NotificacionCobro.DECLINADO
        cobro.save()

        return CreateNotificacionCobro(
            notificacion_cobro=cobro
        )


class LiquidarCobro(graphene.Mutation):
    notificacion_cobro = graphene.Field(NotificacionCobroType)

    class Arguments:
        token = graphene.String(required=True)
        cobro_id = graphene.Int(required=True)
        nip = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, nip, cobro_id):
        def _valida(expr, msg):
            if expr:
                raise Exception(msg)

        cobro = NotificacionCobro.objects.filter(pk=cobro_id)
        _valida(cobro.count() == 0,
                f"No existe cobro con ID {cobro_id}")

        cobro = cobro.first()
        cobro.valida_vencido()

        _valida(cobro.status == NotificacionCobro.VENCIDO,
                'El cobro está vencido.')
        _valida(cobro.status == NotificacionCobro.LIQUIDADO,
                'El cobro ya fue liquidado previamente.')
        _valida(cobro.status == NotificacionCobro.DECLINADO,
                'El cobro ya fue declinado proviamente.')

        beneficiario = cobro.usuario_solicitante
        ordenante = info.context.user
        _valida(ordenante != cobro.usuario_deudor,
                'Tu usuario no coincide con el del cobro')

        _valida(UserProfile.objects.filter(user=ordenante).count() == 0,
                'Usuario sin perfil')
        _valida(not ordenante.Uprofile.password,
                "Usuario no ha establecido nip")
        _valida(not ordenante.Uprofile.check_password(nip),
                'Nip incorrecto')
        _valida(not es_cuenta_inguz(ordenante.Uprofile.cuentaClabe),
                "Cuenta ordenante no es Inguz")
        _valida(not es_cuenta_inguz(beneficiario.Uprofile.cuentaClabe),
                "Cuenta beneficiario no es Inguz")

        fecha = datetime.now()
        claveR = randomString()
        importe = cobro.importe
        monto2F = "{:.2f}".format(round(float(importe), 2))
        status = StatusTrans.objects.get(nombre="exito")
        tipo = TipoTransaccion.objects.get(codigo=20)
        tipo_recibida = TipoTransaccion.objects.get(codigo=21)

        # Actualizamos saldo del usuario
        _valida(float(importe) > ordenante.Uprofile.saldo_cuenta,
                'Saldo insuficiente')
        ordenante.Uprofile.saldo_cuenta -= round(float(importe), 2)
        ordenante.Uprofile.save()
        beneficiario.Uprofile.saldo_cuenta += round(float(importe), 2)
        beneficiario.Uprofile.save()

        concepto = "Liquidacion de cobro"
        main_trans = Transaccion.objects.create(
            user=ordenante,
            fechaValor=fecha,
            monto=float(importe),
            statusTrans=status,
            tipoTrans=tipo,
            concepto=concepto,
            claveRastreo=claveR
        )
        # Padre de la entrada del beneficiario
        user_contacto = cobro.usuario_solicitante
        Transaccion.objects.create(
            user=user_contacto,
            fechaValor=fecha,
            fechaAplicacion=fecha,
            monto=float(importe),
            statusTrans=status,
            tipoTrans=tipo_recibida,
            concepto=concepto,
            claveRastreo=claveR
        )
        inguz_transaccion = InguzTransaction.objects.create(
            monto=monto2F,
            concepto=concepto,
            ordenante=ordenante,
            fechaOperacion=fecha,
            transaccion=main_trans,
        )
        cobro.transaccion = inguz_transaccion
        cobro.status = NotificacionCobro.LIQUIDADO
        cobro.save()

        return CreateNotificacionCobro(
            notificacion_cobro=cobro
        )


class UrlImagenComprobanteInter(graphene.Mutation):

    url = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        id = graphene.Int(required=True)

    def mutate(self, info, token, id):
        user = info.context.user
        if not user.is_anonymous:

            trans = Transaccion.objects.filter(pk=id)
            if trans.count() == 0:
                raise Exception("Transacción inexistente.")
            trans = trans.last()
            if not trans.statusTrans:
                raise Exception("Transacción no genera Comprobante.")
            if trans.statusTrans.nombre != "rechazada":
                raise Exception("Transacción no genera Comprobante.")
            comp = CompTrans(trans)
            url = comp.trans()

            if not settings.USE_S3:
                return UrlImagenComprobanteInter(url=url)

            return UrlImagenComprobanteInter(url=url)


class Mutation(graphene.ObjectType):
    create_transferencia_enviada = CreateTransferenciaEnviada.Field()
    create_notificacion_cobro = CreateNotificacionCobro.Field()
    declinar_cobro = DeclinarCobro.Field()
    liquidar_cobro = LiquidarCobro.Field()
    url_imagen_comprobante_inter = UrlImagenComprobanteInter.Field()
