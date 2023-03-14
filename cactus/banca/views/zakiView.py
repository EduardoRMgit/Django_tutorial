from rest_framework.response import Response
from rest_framework.decorators import api_view
from banca.utils.zaki_comprobacion import ZakiComprobar


@api_view(['POST'])
def ZakiView(request):

    if request.method == 'POST':
        valida = ZakiComprobar(request.data)
    return Response(valida)
