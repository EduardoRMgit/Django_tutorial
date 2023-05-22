from rest_framework.response import Response
from rest_framework.decorators import api_view
from banca.utils.compruebazaki import (
    comprobar_username_curp, comprobar_username, comprobar_curp)


@api_view(['POST'])
def ZakiUsernameCurpView(request):

    if request.method == 'POST':
        valida = comprobar_username_curp(request.data)
    return Response(valida)


@api_view(['POST'])
def ZakiUsernameView(request):

    if request.method == 'POST':
        valida = comprobar_username(request.data)
    return Response(valida)


@api_view(['POST'])
def ZakiCurpView(request):

    if request.method == 'POST':
        valida = comprobar_curp(request.data)
    return Response(valida)
