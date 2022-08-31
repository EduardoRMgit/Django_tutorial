from rest_framework import serializers
from spei.models import StpNotificacionEstadoDeCuenta


class StpNotificacionEstadoDeCuentaSerializer(serializers.ModelSerializer):

    class Meta:
        model = StpNotificacionEstadoDeCuenta
        fields = ['cuenta',
                  'empresa',
                  'estado',
                  'observaciones']
