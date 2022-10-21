import logging

from dapp.models import CodigoCobro
from rest_framework.response import Response
from rest_framework.decorators import api_view


db_logger = logging.getLogger("db")


@api_view(['POST'])
def CodigoCobroView(request):
    if request.method == 'POST':
        # user = request.data["user"]
        # code = request.data["code"]
        # security = request.data["security"]
        cuerpo = {}
        cuerpo['rc'] = 0
        cuerpo['msg'] = "Operación exitosa"
        # cuerpo['user'] = user
        # cuerpo['code'] = code
        # cuerpo['security'] = security
        procesado = cuerpo
        CodigoCobro.objects.create(user='user PRUEBA',
                                   code='code PRUEBA',
                                   security='security PRUEBA',
                                   json=request.data)
        db_logger.info("[DAPP codigoCobro]: {}".format(request.data))
        return Response(procesado)
