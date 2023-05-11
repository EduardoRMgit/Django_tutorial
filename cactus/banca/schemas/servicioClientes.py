import graphene
import logging

from datetime import datetime

from graphql_jwt.decorators import login_required


db_logger = logging.getLogger("db")


class CountServicioClientes(graphene.Mutation):

    detail = graphene.String()

    class Arguments:
        token = graphene.String(required=True)

    @login_required
    def mutate(self, info, token):
        user = info.context.user
        if not user or (user and user.is_anonymous):
            raise Exception('Usuario no válido')

        if user.Uprofile is None:
            raise Exception('Usuario sin perfil')

        try:
            perfil = user.Uprofile
            perfil.contador_servicio_cliente += 1
            perfil.save()
            fecha = datetime.now()
            db_logger.info(
                f"[CountServicioClientes] user: {user}, fecha:{fecha}")
        except Exception as ex:
            db_logger.error(
                f"[CountServicioClientes] ERROR: {ex}")

            raise Exception('Error en el incremento')

        return CountServicioClientes(detail="success")


class Mutation(graphene.ObjectType):
    count_servicio_clientes = CountServicioClientes.Field()
