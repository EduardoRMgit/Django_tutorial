from dapp.models import Reembolso
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['POST'])
def ReembolsoView(request):

    if request.method == 'POST':
        rc = request.data["rc"]
        msg = request.data["msg"]
        data = request.data["data"]
        security = request.data["security"]
        body = {}
        body['rc'] = rc
        body['msg'] = msg
        body['data'] = data
        body['security'] = security
        json = body
        Reembolso.objects.create(rc=rc,
                                 msg=msg,
                                 data=data,
                                 security=security)
        return Response(json)
