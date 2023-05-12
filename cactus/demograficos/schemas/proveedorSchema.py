import graphene
from demograficos.models import Proveedor

from graphene_django.types import DjangoObjectType


class ProveedorType(DjangoObjectType):
    class Meta:
        model = Proveedor


class ProveedorSchema(graphene.Mutation):
    proveedor = graphene.Field(ProveedorType)

    class Arguments:
        token = graphene.String(required=True)
        correo = graphene.String(required=True)
        curp = graphene.String(required=True)
        ocupacion = graphene.String(required=True)
        parentesco = graphene.String(required=True)

    def mutate(
        self, info,
            token,
            correo,
            curp,
            ocupacion,
            parentesco,
    ):
        if curp is not None:
            curp = curp.upper()
            # Agregar validación

        user = info.context.user
        if user.is_anonymous:
            raise AssertionError('usuario no identificado')
        if not user.is_anonymous:
            user.email = correo if correo else user.email
        proveedor = Proveedor.objects.create(
            user=user,
            nombre="from curp",
            apellido_p="from cppurp",
            apellido_m="from curp",
            correo_electronico=correo,
            curp=curp,
            entidad_nacimiento="from curp",
            ocupacion=ocupacion,
            parentesco=parentesco
        )

        return ProveedorSchema(proveedor=proveedor)


class Mutation(graphene.ObjectType):
    create_proveedor = ProveedorSchema.Field()
