from django.urls import path
# from datetime import datetime
from banca.views.transactionView import (TransactionList, TransactionDetail,
                                         cuenta_pdf, comprobante_trans)
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
    path('comprobante_trans/<int:trans_id>/', csrf_exempt(comprobante_trans)),
    path('notificacionestadocuenta/',
         StpNotificacionEstadoCuentaView.as_view())
]
