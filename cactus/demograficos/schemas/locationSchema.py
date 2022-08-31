import graphene

from graphene_django.types import DjangoObjectType

from demograficos.models import GeoLocation, GeoDevice


class GeoLocationType(DjangoObjectType):
    class Meta:
        model = GeoLocation


class GeoDeviceType(DjangoObjectType):
    class Meta:
        model = GeoDevice


class Query(object):
    all_geolocations = graphene.List(GeoLocationType)
    all_geodevices = graphene.List(GeoDeviceType)

    def resolve_all_geolocations(self, info, **kwargs):
        return GeoLocation.objects.all()

    def resolve_all_geodevices(self, info, **kwargs):
        return GeoDevice.objects.all()
