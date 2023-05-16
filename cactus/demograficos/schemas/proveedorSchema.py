import graphene
from demograficos.models import Proveedor
from renapo.renapo_call import check_renapo
from graphene_django.types import DjangoObjectType
from django.conf import settings
from demograficos.utils.stringNormalize import normalize
from demograficos.models import EntidadFed
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

        user = info.context.user
        if user.is_anonymous:
            raise AssertionError('usuario no identificado')

        curp = curp.upper()
        if settings.SITE in ["prod"]:
            data, mensaje = check_renapo(curp)
            if not data:
                raise Exception("Curp no valido")
            try:
                nombre_renapo = normalize(data['nombre_renapo'])
                ap_pat_renapo = normalize(data['ap_pat_renapo'])
                ap_mat_renapo = normalize(data['ap_mat_renapo'])
                fechNac_renapo = data['fechNac_renapo']
                codigo_entidad = curp[11:13]
                entidad_fed = EntidadFed.objects.filter(
                    clave=codigo_entidad)
                if entidad_fed.count() == 0:
                    raise Exception("Entidad de nacimiento no encontrada")
                entidad_fed = entidad_fed.last().entidad

            except Exception as ex:
                db_logger = logging.getLogger('db')
                mensaje = "{} Error: {} / mensaje: {}.".format(
                    "[CONSULTA CURP RENAPO proveedor]", ex, mensaje)
                db_logger.error(mensaje)

        else:
            nombre_renapo = None
            ap_pat_renapo = None
            ap_mat_renapo = None
            fechNac_renapo = None

        proveedor = Proveedor.objects.create(
            user=user,
            nombre=nombre_renapo,
            apellido_p=ap_pat_renapo,
            apellido_m=ap_mat_renapo,
            correo_electronico=correo,
            curp=curp,
            entidad_nacimiento=entidad_fed,
            ocupacion=ocupacion,
            parentesco=parentesco,
            fecha_nacimiento=fechNac_renapo
        )

        return ProveedorSchema(proveedor=proveedor)


class Mutation(graphene.ObjectType):
    create_proveedor = ProveedorSchema.Field()
