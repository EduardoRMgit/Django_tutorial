import graphene
from graphene_django.types import DjangoObjectType

from spei.models import InstitutionBanjico


class InstitutionBanjicoType(DjangoObjectType):
    class Meta:
        model = InstitutionBanjico


class Query(object):
    all_bancos = graphene.List(InstitutionBanjicoType)
    banco = graphene.Field(InstitutionBanjicoType,
                           name=graphene.String(),
                           short_name=graphene.String(),
                           short_id=graphene.String(),
                           long_id=graphene.String())

    def resolve_all_bancos(self, info, **kwargs):
        return InstitutionBanjico.objects.all()

    def resolve_banco(self, info, **kwargs):
        name = kwargs.get('name')
        short_name = kwargs.get('short_name')
        short_id = kwargs.get('short_id')
        long_id = kwargs.get('long_id')

        if name is not None:
            return InstitutionBanjico.objects.get(name=name)

        if short_name is not None:
            return InstitutionBanjico.objects.get(short_name=short_name)

        if short_id is not None:
            return InstitutionBanjico.objects.get(short_id=short_id)

        if long_id is not None:
            return InstitutionBanjico.objects.get(long_id=long_id)

        return None
