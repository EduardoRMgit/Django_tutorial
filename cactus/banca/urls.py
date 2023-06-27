from django.urls import path
# from datetime import datetime
from banca.views.transactionView import (TransactionList, TransactionDetail,
                                         cuenta_pdf)
from banca.views.zakiViews import (ZakiCurpView, ZakiUsernameView,
                                   ZakiLoanView, ZakiPayView,
                                   ZakiClabeCurpView)
from spei.views import StpNotificacionEstadoCuentaView

from django.views.decorators.csrf import csrf_exempt


# class DateConverter:
#     regex = '\d{4}-\d{2}-\d{2}'

#     def to_python(self, value):
#         return datetime.strptime(value, '%Y-%m-%d')

#     def to_url(self, value):
#         return value


# register_converter(DateConverter, 'yyyy')

urlpatterns = [
    path('sendabono/', TransactionList.as_view()),
    path('estado/', TransactionDetail.as_view()),
    path('cuenta/', csrf_exempt(cuenta_pdf)),
    path('notificacionestadocuenta/',
         StpNotificacionEstadoCuentaView.as_view()),
    path('validacurp/', ZakiCurpView),
    path('validaclabecurp/', ZakiClabeCurpView),
    path('validausername/', ZakiUsernameView),
    path('creaprestamo/', ZakiLoanView),
    path('liquidaprestamo/', ZakiPayView)
]
