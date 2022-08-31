from rest_framework import serializers
from scotiabank.models import RespuestaScotia


class RespuestaScotiaSerializer(serializers.ModelSerializer):
    url_respuesta = serializers.URLField(max_length=2056, allow_blank=True)

    class Meta:
        model = RespuestaScotia
        fields = ('id',
                  'fecha',
                  'url_respuesta')
