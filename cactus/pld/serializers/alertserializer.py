from rest_framework import serializers
from pld.models import AlertasPLD


class AlertaSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlertasPLD
        fields = [
            'descripcion',
            'motivo'
        ]
