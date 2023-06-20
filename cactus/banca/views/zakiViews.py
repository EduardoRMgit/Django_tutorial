from rest_framework.response import Response
from rest_framework.decorators import api_view
from banca.utils.compruebazaki import (
    comprobar_username_curp, comprobar_username, comprobar_curp,
    comprobar_clabe_curp)
from banca.utils.pago_prestamo_zaki import crear_prestamo, liquidar_prestamo


def __c_back_zaki(f, request):
    print("request: ", request)
    if request.method == 'POST':
        valida = f(request.data)
    return Response(valida)


@api_view(['POST'])
def ZakiUsernameCurpView(request):
    return __c_back_zaki(comprobar_username_curp, request)


@api_view(['POST'])
def ZakiClabeCurpView(request):
    return __c_back_zaki(comprobar_clabe_curp, request)


@api_view(['POST'])
def ZakiUsernameView(request):
    return __c_back_zaki(comprobar_username, request)


@api_view(['POST'])
def ZakiCurpView(request):
    return __c_back_zaki(comprobar_curp, request)


@api_view(['POST'])
def ZakiLoanView(request):
    return __c_back_zaki(crear_prestamo, request)


@api_view(['POST'])
def ZakiPayView(request):
    return __c_back_zaki(liquidar_prestamo, request)
