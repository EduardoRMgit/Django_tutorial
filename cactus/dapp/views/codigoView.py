from dapp.models import CodigoCobro
from rest_framework.response import Response
from rest_framework.decorators import api_view
import logging


@api_view(['POST'])
def CodigoCobroView(request):
    db_logger = logging.getLogger("db")

    if request.method == 'POST':
        user = request.data["user"]
        code = request.data["code"]
        security = request.data["security"]
        cuerpo = {}
        cuerpo['rc'] = '0'
        cuerpo['msg'] = 'OK'
        cuerpo['user'] = user
        cuerpo['code'] = code
        cuerpo['security'] = security
        procesado = cuerpo
        CodigoCobro.objects.create(user=user,
                                   code=code,
                                   security=security,
                                   json=request.data)
        db_logger.info(request.data)
        return Response(procesado)
