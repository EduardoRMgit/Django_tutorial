import graphene
from datetime import datetime, timedelta
from spei.stpTools import randomString

from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from banca.models import (InguzTransaction, StatusTrans, TipoTransaccion,
                          Transaccion)
from demograficos.models.userProfile import UserProfile
from demograficos.models import Contacto
from banca.schemas.transaccionSchema import UserType


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

    @login_required
    def mutate(self,
               info,
               token,
               contacto,
               abono,
               concepto,
               nip,):

        try:
            ordenante = info.context.user
        except Exception:
            raise Exception('Usuario inexistente')
        if ordenante.Uprofile.cuentaClabe[:10] != "6461802180":
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

        if contacto.clabe[:10] != "6461802180":  # Inguz
            raise Exception("Cuenta de beneficiario no es inguz")

        if float(abono) <= 0:
            raise Exception("El abono debe ser mayor a cero")

        user_contacto = UserProfile.objects.get(
                cuentaClabe=contacto.clabe, status="O").user

        fecha = (datetime.now() +
                 timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
        claveR = randomString()
        monto2F = "{:.2f}".format(float(abono))
        status = StatusTrans.objects.get(nombre="exito")
        tipo = TipoTransaccion.objects.get(codigo=2)

        # Actualizamos saldo del usuario
        if float(abono) <= ordenante.Uprofile.saldo_cuenta:
            ordenante.Uprofile.saldo_cuenta -= float(abono)
            ordenante.Uprofile.save()
        else:
            raise Exception("Saldo insuficiente")

        user_contacto.Uprofile.saldo_cuenta += float(abono)
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
            transaccion=main_trans
        )

        print(f"transacción creada: {inguz_transaccion.__dict__}")

        return CreateInguzTransaccion(
            inguz_transaccion=inguz_transaccion,
            user=ordenante
        )


# 4
class Mutation(graphene.ObjectType):
    create_inguz_transaccion = CreateInguzTransaccion.Field()
