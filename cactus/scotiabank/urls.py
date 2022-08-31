from django.urls import path
from scotiabank.views import (RespuestaScotiaView,
                              RespuestaScotiaDetailView)

urlpatterns = [
    path(
        'scotiabank/archivo/respuesta/',
        RespuestaScotiaView.as_view(),
        name='Respuesta'),
    path(
        'scotiabank/archivo/respuesta/<int:id>/',
        RespuestaScotiaDetailView.as_view(),
        name='RespuestaDetail')
]
