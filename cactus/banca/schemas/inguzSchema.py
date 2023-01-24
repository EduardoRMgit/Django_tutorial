import graphene
import logging

from django.utils import timezone

from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from banca.utils.clabe import es_cuenta_inguz
from banca.schemas.transaccionSchema import UserType
from banca.models import (InguzTransaction, StatusTrans, TipoTransaccion,
                          Transaccion, NotificacionCobro)
from demograficos.models.userProfile import UserProfile
from demograficos.models import Contacto
from spei.stpTools import randomString
from django.conf import settings


URL_IMAGEN = settings.URL_IMAGEN


class InguzType(DjangoObjectType):
    class Meta:
        model = InguzTransaction


class CreateInguzTransaccion(graphene.Mutation):
    inguz_transaccion = graphene.Field(InguzType)
    user = graphene.Field(UserType)

    class Arguments:
        token = graphene.String(required=True)
        contacto = graphene.Int(required=True)
        abono = graphene.String(required=True)
        concepto = graphene.String(required=True)
        nip = graphene.String(required=True)
        cobro_id = graphene.Int()

    @login_required
    def mutate(self,
               info,
               token,
               contacto,
               abono,
               concepto,
               nip,
               cobro_id=None):
        db_logger = logging.getLogger("db")
        try:
            ordenante = info.context.user
        except Exception:
            raise Exception('Usuario inexistente')
        if not es_cuenta_inguz(ordenante.Uprofile.cuentaClabe):
            raise Exception("Cuenta ordenante no es Inguz")
        if UserProfile.objects.filter(user=ordenante).count() == 0:
            raise Exception('Usuario sin perfil')
        if not ordenante.Uprofile.password:
            raise Exception("Usuario no ha establecido nip")
        if not ordenante.Uprofile.check_password(nip):
            raise Exception('Nip incorrecto')

        try:
            contacto = Contacto.objects.get(pk=contacto,
                                            verificacion="O",
                                            user=ordenante,
                                            activo=True,
                                            bloqueado=False)
        except Exception:
            raise Exception("Contacto no válido")

        if not es_cuenta_inguz(contacto.clabe):  # Inguz
            raise Exception("Cuenta de beneficiario no es inguz")

        if float(abono) <= 0:
            raise Exception("El abono debe ser mayor a cero")

        try:
            user_contacto = UserProfile.objects.get(
                cuentaClabe=contacto.clabe,
                status="O",
                enrolamiento=True).user
        except Exception:
            raise Exception("La cuenta destino está fuera de servicio")
        fecha = timezone.now()
        claveR = randomString()
        monto2F = "{:.2f}".format(round(float(abono), 2))
        status = StatusTrans.objects.get(nombre="exito")
        tipo = TipoTransaccion.objects.get(codigo=18)
        tipo_recibida = TipoTransaccion.objects.get(codigo=19)

        # Actualizamos saldo del usuario
        if float(abono) <= ordenante.Uprofile.saldo_cuenta:
            ordenante.Uprofile.saldo_cuenta -= round(float(abono), 2)
            ordenante.Uprofile.save()
        else:
            raise Exception("Saldo insuficiente")

        user_contacto.Uprofile.saldo_cuenta += round(float(abono), 2)
        user_contacto.Uprofile.save()
        main_trans = Transaccion.objects.create(
            user=ordenante,
            fechaValor=fecha,
            fechaAplicacion=fecha,
            monto=float(abono),
            statusTrans=status,
            tipoTrans=tipo,
            concepto=concepto,
            claveRastreo=claveR
        )

        inguz_transaccion = InguzTransaction.objects.create(
            monto=monto2F,
            concepto=concepto.split(' - ')[-1],
            ordenante=ordenante,
            fechaOperacion=fecha,
            contacto=contacto,
            transaccion=main_trans,
        )

        # Recibida (sin transacción hija)
        Transaccion.objects.create(
            user=user_contacto,
            fechaValor=fecha,
            fechaAplicacion=fecha,
            monto=float(abono),
            statusTrans=status,
            tipoTrans=tipo_recibida,
            concepto=concepto,
            claveRastreo=claveR
        )

        if cobro_id is not None:
            cobro = NotificacionCobro.objects.filter(pk=cobro_id)
            if cobro.count() == 0:
                raise Exception(f"No existe cobro con ID {cobro_id}")
            cobro = cobro.first()
            cobro.status = NotificacionCobro.LIQUIDADO
            cobro.transaccion = inguz_transaccion
            cobro.save()

        print(f"transacción creada: {inguz_transaccion.__dict__}")
        msg = "[Inguz_Inguz] Transaccion exitosa del usuario: {} \
            con cuenta: {} \
            a la cuenta: {} \
            por: ${}".format(
            ordenante.username,
            ordenante.Uprofile.cuentaClabe,
            contacto.clabe,
            monto2F
        )
        contacto.frecuencia = int(contacto.frecuencia) + 1
        contacto.save()
        db_logger.info(msg)
        return CreateInguzTransaccion(
            inguz_transaccion=inguz_transaccion,
            user=ordenante
        )


class UrlImagenComprobanteInguz(graphene.Mutation):

    url = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, token, id):
        user = info.context.user
        if not user.is_anonymous:
            transaccion = InguzTransaction.objects.get(id=id)
            transaccion.comprobante_img = URL_IMAGEN
            transaccion.url_comprobante = URL_IMAGEN
            transaccion.save()
            url = transaccion.url_comprobante
            return UrlImagenComprobanteInguz(url=url)


class UrlImagenComprobanteCobro(graphene.Mutation):

    url = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        id = graphene.Int(required=True)
        tipo_comprobante = graphene.String()

    @login_required
    def mutate(self, info, token, id, tipo_comprobante):
        user = info.context.user
        if not user.is_anonymous:
            if tipo_comprobante == "notificacion":
                try:
                    transaccion = NotificacionCobro.objects.get(
                        id=id)
                    url = URL_IMAGEN
                except Exception:
                    raise Exception("id de cobro no válido")
            elif tipo_comprobante == "pago":
                try:
                    transaccion = NotificacionCobro.objects.get(id=id)
                except Exception:
                    raise Exception("id de cobro no válido")
                if transaccion.status == "L":
                    url = URL_IMAGEN
                else:
                    raise Exception("Cobro no liquidado")
            else:
                raise Exception(
                    "Ingrese un tipo válido ('notificacion' "
                    "o 'pago')."
                )
            return UrlImagenComprobanteCobro(url=url)


# 4
class Mutation(graphene.ObjectType):
    create_inguz_transaccion = CreateInguzTransaccion.Field()
    url_imagen_comprobante_inguz = UrlImagenComprobanteInguz.Field()
    url_imagen_comprobante_cobro = UrlImagenComprobanteCobro.Field()
