import logging

from dapp.models import Reembolso
from rest_framework.response import Response
from rest_framework.decorators import api_view


db_logger = logging.getLogger("db")


@api_view(['POST'])
def ReembolsoView(request):
    if request.method == 'POST':
        # rc = request.data["rc"]
        # msg = request.data["msg"]
        # data = request.data["data"]
        # security = request.data["security"]
        body = {}
        body['rc'] = 0
        body['msg'] = "Operación exitosa"
        # body['data'] = data
        # body['security'] = security
        json = body
        Reembolso.objects.create(rc='0',
                                 msg='PRUEBA',
                                 data='Data PRUEBA',
                                 security='Security PRUEBA')
        db_logger.info("[DAPP reembolso]: {}".format(request.data))
        return Response(json)
