from rest_framework import generics
from pld.serializers import AlertaSerializer
from pld.models import AlertasPLD
from django.utils import timezone
import logging


class AlertasPLDView(generics.ListCreateAPIView):

    serializer_class = AlertaSerializer
    queryset = AlertasPLD.objects.all()

    def post(self, request, *args, **kwargs):
        db_logger = logging.getLogger("db")
        msg_logg = "{} con fecha {}: {}".format(
                    "[Alerta PLD] (post)",
                    timezone.now(),
                    request.POST)
        print(msg_logg)
        db_logger.info(msg_logg)
        return super().post(request, *args, **kwargs)
