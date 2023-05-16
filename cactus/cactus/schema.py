import graphene
import graphql_jwt
from servicios.schemas import productoSchema, GpoTRansaccionSchema
from legal.schemas import legalSchema
from banca.schemas import (transaccionSchema, inguzSchema, ScotiaSchema,
                           creacionSchema, servicioClientes)
from demograficos.schemas import (userProfileSchema,
                                  telefonoSchema,
                                  tarjetaSchema,
                                  institucionesSchema,
                                  documentosSchema,
                                  direccionSchema,
                                  locationSchema,
                                  proveedorSchema)
from spei.schemas import listabancosSchema
from seguros.schemas import asignar_seguro
from dde.schemas import (createddeSchema, imagenesddeSchema)
from crecimiento.schemas import crecimientoSchema
from pagos.rapydcollect import schemacollect
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType
from graphql_jwt import mixins
from demograficos.models import UserProfile
from django.contrib.auth import get_user_model
from cactus.utils import token_auth, unblock_account
from django.utils import timezone
from datetime import timedelta
from arcus.schemas import arcusbills


__all__ = [
    "JSONWebTokenMutationP",
]


class JSONWebTokenMutationP(mixins.ObtainJSONWebTokenMixin, graphene.Mutation):
    class Meta:
        abstract = True

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments.update(
            {
                get_user_model().USERNAME_FIELD: graphene.String(
                    required=True),
                "password": graphene.String(required=True),
            },
        )
        return super().Field(*args, **kwargs)

    @classmethod
    @token_auth
    def mutate(cls, root, info, **kwargs):
        return cls.resolve(root, info, **kwargs)


class UserType2(DjangoObjectType):
    class Meta:
        model = User


class ObtainToken(JSONWebTokenMutationP):
    user = graphene.Field(UserType2)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        user_ = kwargs["username"]
        _user_ = User.objects.get(username=user_)
        time_ = _user_.Uprofile.blocked_date
        compare = timezone.now()
        is_active = _user_.Uprofile.is_active
        try:
            unblock_account(_user_, time_)
            _user_ = UserProfile.objects.get(user=_user_, status="O")
            if is_active is True:
                return cls(user=info.context.user)
            else:
                return Exception("Inactive User")
        except Exception as ex:
            user_ = UserProfile.objects.get(user=_user_)
            if user_.status == "B":
                pasado = (compare - time_)
                restante = timedelta(minutes=5) - pasado
                contador = str(restante)
                minutos = int(contador[3:4])+1
                if minutos == 1:
                    minuto = "minuto"
                else:
                    minuto = "minutos"
                return Exception(
                    f"Cuenta Bloqueada intenta en: {minutos} {minuto}")
            elif user_.status == "C":
                return Exception("Cuenta Cancelada")
            return ex


class Query(transaccionSchema.Query,
            productoSchema.Query,
            userProfileSchema.Query,
            telefonoSchema.Query,
            tarjetaSchema.Query,
            institucionesSchema.Query,
            direccionSchema.Query,
            documentosSchema.Query,
            legalSchema.Query,
            listabancosSchema.Query,
            locationSchema.Query,
            schemacollect.Query,
            ScotiaSchema.Query,
            creacionSchema.Query,
            crecimientoSchema.Query,
            arcusbills.Query,
            graphene.ObjectType):
    pass


class Mutation(transaccionSchema.Mutation,
               userProfileSchema.Mutation,
               direccionSchema.Mutation,
               documentosSchema.Mutation,
               legalSchema.Mutation,
               telefonoSchema.Mutation,
               asignar_seguro.Mutation,
               GpoTRansaccionSchema.Mutation,
               createddeSchema.Mutation,
               imagenesddeSchema.Mutation,
               schemacollect.Mutation,
               inguzSchema.Mutation,
               ScotiaSchema.Mutation,
               crecimientoSchema.Mutation,
               arcusbills.Mutation,
               servicioClientes.Mutation,
               proveedorSchema.Mutation,
               graphene.ObjectType):
    token_auth = ObtainToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
