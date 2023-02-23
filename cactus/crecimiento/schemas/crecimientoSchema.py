import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from demograficos.schemas.userProfileSchema import ContactosType

from django.db.models import Q

from demograficos.models import Contacto, UserProfile
from crecimiento.models import PodcastLink
from crecimiento.models import Respaldo


class ExtendedConnection(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()
    edge_count = graphene.Int()

    def resolve_total_count(root, info, **kwargs):
        return root.length

    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)


class PodcastLinkType(DjangoObjectType):
    class Meta:
        model = PodcastLink

    def resolve_imagen(self, info):
        return ((self.imagen.url).split("?")[0])


class RespaldoType(DjangoObjectType):

    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = Respaldo
        filter_fields = {
            'status': ['exact', ],
            'activo': ['exact', ],
            'ordenante': ['exact', ],
            'respaldo': ['exact', ]
        }
        interfaces = (graphene.Node, )
        connection_class = ExtendedConnection


class Query(object):

    all_podcastLink = graphene.List(
        PodcastLinkType,
        description="Query all the objects from the \
        PodcastLink Model"
    )

    all_respaldos = DjangoFilterConnectionField(
        RespaldoType,
        token=graphene.String(required=True),
        ordering=graphene.String(),
        description="Query all the objects from the \
        Respaldo Model"
    )

    def resolve_all_podcastLink(self, info, **kwargs):
        return PodcastLink.objects.filter(activo=True)

    @login_required
    def resolve_all_respaldos(self, info, ordering=None, **kwargs):
        user = info.context.user
        print(user)
        qs = Respaldo.objects.filter(
            Q(ordenante=user) |
            Q(respaldo=user)
        )
        for respaldo in qs:
            if respaldo.status == 'P':
                respaldo.valida_vencido()

        if ordering:
            qs = qs.order_by(ordering)
        return (qs)


class CreateRespaldo(graphene.Mutation):

    agregados = graphene.List(RespaldoType)
    errores = graphene.List(ContactosType)

    class Arguments:
        token = graphene.String(required=True)
        nip = graphene.String(required=True)
        contacto_list = graphene.List(graphene.Int, required=True)

    @login_required
    def mutate(self, info, token, nip, contacto_list):

        errores = []
        agregados = []

        user = info.context.user
        up = user.Uprofile
        if not up.check_password(nip):
            raise Exception("El NIP es incorrecto")

        if len(contacto_list) > 5:
            raise Exception("No pueden seleccionarse mas de 5 contactos")

        for contacto in contacto_list:
            try:
                contacto = Contacto.objects.get(
                    user=user,
                    id=contacto,
                    es_inguz=True,
                    bloqueado=False,
                    activo=True
                )
            except Exception:
                raise Exception("Uno o más contactos inválidos")
            try:
                respaldo = UserProfile.objects.get(
                                cuentaClabe=contacto.clabe,
                                status="O").user
            except Exception:
                errores.append(contacto.id)
                continue
            existe = Respaldo.objects.filter(
                Q(
                    ordenante=user,
                    respaldo=respaldo,
                    activo=True
                ) |
                Q(
                    ordenante=respaldo,
                    respaldo=user,
                    activo=True
                )
            )
            bloqueado = Contacto.objects.filter(
                user=respaldo,
                clabe=user.Uprofile.cuentaClabe,
                bloqueado=True,
                activo=True
            )
            espacio_user = Respaldo.objects.filter(
                Q(ordenante=user, activo=True) |
                Q(respaldo=user, activo=True)
            )
            espacio_respaldo = Respaldo.objects.filter(
                Q(ordenante=respaldo, activo=True) |
                Q(respaldo=respaldo, activo=True)
            )

            if espacio_user.count() >= 5:
                raise Exception("UserLimitEx")

            if espacio_respaldo.count() >= 5:
                errores.append(contacto.id)
                continue

            if bloqueado:
                errores.append(contacto.id)
                continue

            if not existe:
                try:
                    agregado = Respaldo.objects.create(
                        status="P",
                        ordenante=user,
                        respaldo=respaldo,
                        contacto_id=contacto.id,
                        contrato=None
                    )
                    agregados.append(agregado.id)
                except Exception:
                    errores.append(contacto.id)
                    continue
            else:
                errores.append(contacto.id)
                continue

        if agregados:
            agregados = Respaldo.objects.filter(id__in=agregados)
        if errores:
            errores = Contacto.objects.filter(id__in=errores)
        return CreateRespaldo(
            agregados=agregados,
            errores=errores
        )


class ConfirmRespaldo(graphene.Mutation):

    respaldo = graphene.Field(RespaldoType)

    class Arguments:
        token = graphene.String(required=True)
        nip = graphene.String(required=True)
        respaldo = graphene.Int(required=True)
        aceptar = graphene.Boolean(required=True)

    @login_required
    def mutate(self, info, token, nip, respaldo, aceptar):

        user = info.context.user
        up = user.Uprofile
        if not up.check_password(nip):
            raise Exception("El NIP es incorrecto")

        try:
            respaldo = Respaldo.objects.get(
                id=respaldo,
                status="P",
                respaldo=user,
                activo=True
            )
        except Exception:
            raise Exception("Datos inválidos")

        if aceptar:
            if respaldo.status == "P":
                respaldo.status = "A"
            else:
                raise Exception("Invitación Inválida")
        else:
            respaldo.status = "D"
            respaldo.activo = False
        respaldo.save()

        return ConfirmRespaldo(
            respaldo=respaldo
        )


class DeleteRespaldo(graphene.Mutation):

    respaldo = graphene.Field(RespaldoType)

    class Arguments:
        token = graphene.String(required=True)
        nip = graphene.String(required=True)
        respaldo = graphene.Int(required=True)

    @login_required
    def mutate(self, info, token, nip, respaldo):

        user = info.context.user
        up = user.Uprofile
        if not up.check_password(nip):
            raise Exception("El NIP es incorrecto")

        try:
            respaldo = Respaldo.objects.get(
                Q(
                    id=respaldo,
                    ordenante=user,
                    activo=True
                ) |
                Q(
                    id=respaldo,
                    respaldo=user,
                    activo=True
                )
            )
        except Exception:
            raise Exception("Datos inválidos")

        respaldo.activo = False
        respaldo.save()

        return DeleteRespaldo(
            respaldo=respaldo
        )


class Mutation(graphene.ObjectType):
    create_respaldo = CreateRespaldo.Field()
    confirm_respaldo = ConfirmRespaldo.Field()
    delete_respaldo = DeleteRespaldo.Field()
