import graphene
from demograficos.models import Proveedor
from renapo.renapo_call import check_renapo
from graphene_django.types import DjangoObjectType
from django.conf import settings
from demograficos.utils.stringNormalize import normalize
import logging


db_logger = logging.getLogger("db")


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
        if settings.SITE in ["prod"]:
            data, mensaje = check_renapo(curp)
        else:
            data = {
                'nombre_renapo': "None",
                'ap_pat_renapo': "None",
                'ap_mat_renapo': "None",
                'fechNac_renapo': "None"
            }
            mensaje = ""
        try:
            if data:
                nombre_renapo = normalize(data['nombre_renapo'])
                ap_pat_renapo = normalize(data['ap_pat_renapo'])
                ap_mat_renapo = normalize(data['ap_mat_renapo'])
                fechNac_renapo = data['fechNac_renapo']
        except Exception as ex:
            db_logger = logging.getLogger('db')
            mensaje = "[CONSULTA CURP RENAPO] Falló la validación. Error: \
                {} / mensaje: {}.".format(ex, mensaje)
            db_logger.error(mensaje)
        user = info.context.user
        if user.is_anonymous:
            raise AssertionError('usuario no identificado')
        if not user.is_anonymous:
            user.email = correo if correo else user.email
        proveedor = Proveedor.objects.create(
            user=user,
            nombre=nombre_renapo,
            apellido_p=ap_pat_renapo,
            apellido_m=ap_mat_renapo,
            correo_electronico=correo,
            curp=curp,
            entidad_nacimiento=fechNac_renapo,
            ocupacion=ocupacion,
            parentesco=parentesco
        )

        return ProveedorSchema(proveedor=proveedor)


class Mutation(graphene.ObjectType):
    create_proveedor = ProveedorSchema.Field()
