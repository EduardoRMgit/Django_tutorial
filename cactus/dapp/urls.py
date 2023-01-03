from django.urls import path
from dapp.views import CodigoCobroView, ReembolsoView

urlpatterns = [
    path('dapp/sendcodigo/', CodigoCobroView, name='sendcodigo'),
    path('dapp/reembolso/', ReembolsoView, name='reembolso'),
]
