from rest_framework import serializers
from demograficos.models import DocAdjunto


class ImageDocSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocAdjunto
        exclude = ['ruta', 'orden']
