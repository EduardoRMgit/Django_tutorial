from rest_framework.response import Response
from rest_framework.decorators import api_view
from cactus.banca.utils.compruebacurp import comprobar_curp


@api_view(['POST'])
def ZakiCurpView(request):

    if request.method == 'POST':
        valida = comprobar_curp(request.data)
    return Response(valida)
