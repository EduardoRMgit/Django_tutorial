import graphene
from spei.models import StpTransaction
from graphene_django.types import DjangoObjectType
from spei.cep import url_cep


class UrlCepType(DjangoObjectType):
    class Meta:
        model = StpTransaction


class Query(graphene.ObjectType):
    cep = graphene.Field(UrlCepType,
                         id=graphene.Int(required=True),
                         token=graphene.String())

    def resolve_cep(self, info, id, **kwargss):
        transaccion = StpTransaction.objects.get(id=id)
        url = url_cep(transaccion)
        if url:
            transaccion.url_cep = url
            transaccion.save()
        return transaccion
