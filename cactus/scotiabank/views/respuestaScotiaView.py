from rest_framework import generics
from rest_framework.response import Response
from django.http import Http404
from scotiabank.models import RespuestaScotia
from scotiabank.serializers import RespuestaScotiaSerializer


class RespuestaScotiaView(generics.ListCreateAPIView):

    serializer_class = RespuestaScotiaSerializer
    queryset = RespuestaScotia.objects.all()


class RespuestaScotiaDetailView(generics.ListAPIView):

    def get_object(self, id):
        try:
            return RespuestaScotia.objects.get(id=id)
        except RespuestaScotia.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        Entidades = self.get_object(id)
        serializer = RespuestaScotiaSerializer(Entidades)
        return Response(serializer.data)
