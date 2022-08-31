# from PaySenseiCore.models.stp import StpTransaction
# from PaySenseiCore.serializers import StpResponseSerializer
# from rest_framework.generics import UpdateAPIView

import logging

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
# from ..custom_permissions import StpUserPermission

from spei.serializers import StpNotificacionEstadoDeCuentaSerializer
# from spei.models import StpNotificacionEstadoDeCuenta


db_logger = logging.getLogger('db')


# class StpTransactionUpdater(UpdateAPIView):

#     queryset = StpTransaction.objects.all()
#     serializer_class = StpResponseSerializer
#     lookup_field = 'stpId'


class StpNotificacionEstadoCuentaView(CreateAPIView):
    # queryset = StpNotificacionEstadoDeCuenta.objects.all()
    serializer_class = StpNotificacionEstadoDeCuentaSerializer

    def post(self, request):
        """
        Notificación de confirmación de registro de cuenta STP
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        notificacion = serializer.save()

        db_logger.info("[STP StpNotificacionEstadoCuentaView] {}".format(
            notificacion.cuenta))

        return Response({"mensaje": "recibido"})
