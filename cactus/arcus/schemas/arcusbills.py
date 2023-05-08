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
    services_bills = graphene.List(ServicesType,
                                   tipo=graphene.String(),
                                   nombre=graphene.String())
    recargas_bills = graphene.List(RecargasType)

    @login_required
    def resolve_services_bills(root, info, tipo=None, nombre=None, **kwargs):
        all = ServicesArcus.objects.all()
        if nombre:
            try:
                return all.filter(name=nombre)
            except Exception:
                raise Exception("Compañia no existe.")
        if tipo:
            return all.filter(biller_type=tipo)
        return all

    @login_required
    def resolve_recargas_bills(root, info, **kwargs):
        return RecargasArcus.objects.all()
