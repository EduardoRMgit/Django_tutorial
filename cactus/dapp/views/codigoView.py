from dapp.models import CodigoCobro
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['POST'])
def CodigoCobroView(request):

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
                                   security=security)
        return Response(procesado)
