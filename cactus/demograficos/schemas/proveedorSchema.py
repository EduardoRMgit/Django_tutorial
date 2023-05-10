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
        nombre = graphene.String(required=True)
        apellido_p = graphene.String(required=True)
        apellido_m = graphene.String(required=True)
        correo = graphene.String(required=True)
        curp = graphene.String(required=True)
        entidad_nacimiento = graphene.String(required=True)
        ocupacion = graphene.String(required=True)
        parentesco = graphene.String(required=True)
        fecha_nacimiento = graphene.Date(required=True)

    def mutate(
        self, info, token,
        nombre,
        apellido_p,
        apellido_m,
        correo,
        curp,
        entidad_nacimiento,
        ocupacion,
        parentesco,
        fecha_nacimiento
    ):
        if nombre is not None:
            nombre = nombre.strip()
        if apellido_m is not None:
            apellido_m = apellido_m.strip()
        if apellido_p is not None:
            apellido_p = apellido_p.strip()
        if curp is not None:
            curp = curp.upper()
        user = info.context.user
        if user.is_anonymous:
            raise AssertionError('usuario no identificado')
        if not user.is_anonymous:
            user.email = correo if correo else user.email
        proveedor = Proveedor.objects.create(
            user=user,
            nombre=nombre,
            apellido_p=apellido_p,
            apellido_m=apellido_m,
            correo_electronico=correo,
            curp=curp,
            entidad_nacimiento=entidad_nacimiento,
            ocupacion=ocupacion,
            parentesco=parentesco,
            fecha_nacimiento=fecha_nacimiento,
        )

        return ProveedorSchema(proveedor=proveedor)


class Mutation(graphene.ObjectType):
    create_proveedor = ProveedorSchema.Field()
