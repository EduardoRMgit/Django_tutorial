import graphene
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType
from arcus.models import ServicesArcus, RecargasArcus


class ServicesType(DjangoObjectType):
    class Meta:
        model = ServicesArcus


class RecargasType(DjangoObjectType):
    class Meta:
        model = RecargasArcus


class Query(object):
    services_bills = graphene.List(ServicesType)
    recargas_bills = graphene.List(RecargasType)

    @login_required
    def resolve_services_bills(root, info, **kwargs):
        return ServicesArcus.objects.all()

    @login_required
    def resolve_recargas_bills(root, info, **kwargs):
        return RecargasArcus.objects.all()
