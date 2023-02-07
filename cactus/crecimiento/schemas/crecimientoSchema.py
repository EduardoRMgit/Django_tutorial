import graphene
from graphene_django.types import DjangoObjectType

from crecimiento.models import Bartola


class BartolaType(DjangoObjectType):
    class Meta:
        model = Bartola


class Query(object):

    all_bartola = graphene.List(
        BartolaType,
        description="`Query a single object from \
        PdfLegalType Model:` using pdfLegalId(pk)"
    )

    def resolve_all_bartola(self, info, **kwargs):
        return Bartola.objects.filter(activo=True)


class Mutation(graphene.ObjectType):
    pass
