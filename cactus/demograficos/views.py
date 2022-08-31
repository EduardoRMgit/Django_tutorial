from demograficos.serializers import ImageDocSerializer
from rest_framework import generics


class ImageDoc(generics.CreateAPIView):
    serializer_class = ImageDocSerializer
