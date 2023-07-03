import graphene
from demograficos.models import VersionApp
from graphene_django.types import DjangoObjectType


class VersionAppType(graphene.ObjectType):
    estatus = graphene.String()


class UrlAppType(DjangoObjectType):
    class Meta:
        model = VersionApp
    fields = ['url_android', 'url_ios']


class Query(object):
    version_app = graphene.Field(VersionAppType,
                                 version=graphene.String(required=True))
    url_app = graphene.Field(UrlAppType)

    def resolve_version_app(self, info, **kwargs):
        version = kwargs.get('version')
        version_v = VersionApp.objects.filter(
            version=version, activa=True).last()
        estado = {}
        if not version_v:
            estado["estatus"] = "Error de version"
            raise Exception(estado)
        else:
            estado["estatus"] = "Success"
            return estado

    def resolve_url_app(self, info, **kwargs):
        return VersionApp.objects.filter(activa=True).last()
