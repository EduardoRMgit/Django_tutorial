import graphene
import logging

from django.utils import timezone

from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from banca.utils.clabe import es_cuenta_inguz
from banca.schemas.transaccionSchema import UserType
from banca.models import (InguzTransaction, StatusTrans, TipoTransaccion,
                          Transaccion)
from demograficos.models.userProfile import UserProfile
from demograficos.models import Contacto
from spei.stpTools import randomString
from django.core.files.images import ImageFile


class InguzType(DjangoObjectType):
    class Meta:
        model = InguzTransaction


class Query(graphene.ObjectType):
    url_imagen_comprobante_inguz = graphene.List(InguzType,
                                    token=graphene.String(required=True),
                                    id_transaccion=graphene.Int(
                                        required=True))

    def resolve_url_imagen_comprobante_inguz(self, info, **kwargs):
        id = kwargs.get("id_transaccion")
        transaccion = InguzTransaction.objects.filter(id=id)
        trans = transaccion.count()
        if trans != 0:
            return InguzTransaction.objects.filter(id=id)
        else:
            raise Exception("Transaccion Invalida")


class CreateInguzTransaccion(graphene.Mutation):
    inguz_transaccion = graphene.Field(InguzType)
    user = graphene.Field(UserType)

    class Arguments:
        token = graphene.String(required=True)
        contacto = graphene.Int(required=True)
        abono = graphene.String(required=True)
        concepto = graphene.String(required=True)
        nip = graphene.String(required=True)

    @login_required
    def mutate(self,
               info,
               token,
               contacto,
               abono,
               concepto,
               nip,):
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
                                            user=ordenante)
        except Exception:
            raise Exception("Contacto no valido")

        if not es_cuenta_inguz(contacto.clabe):  # Inguz
            raise Exception("Cuenta de beneficiario no es inguz")

        if float(abono) <= 0:
            raise Exception("El abono debe ser mayor a cero")

        user_contacto = UserProfile.objects.get(
            cuentaClabe=contacto.clabe, status="O").user
        fecha = timezone.now()
        claveR = randomString()
        monto2F = "{:.2f}".format(round(float(abono), 2))
        status = StatusTrans.objects.get(nombre="exito")
        tipo = TipoTransaccion.objects.get(codigo=13)

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
            comprobante_img=ImageFile(open("Zygoovertical-01.jpg", "rb"))
        )

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
        contacto = Contacto.objects.get(pk=contacto.id,
                                        verificacion="O",
                                        user=ordenante)
        contacto.frecuencia = int(contacto.frecuencia) + 1
        contacto.save()
        db_logger.info(msg)
        return CreateInguzTransaccion(
            inguz_transaccion=inguz_transaccion,
            user=ordenante
        )


# 4
class Mutation(graphene.ObjectType):
    create_inguz_transaccion = CreateInguzTransaccion.Field()
