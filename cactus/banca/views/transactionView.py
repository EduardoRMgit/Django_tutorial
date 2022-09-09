import os
import io
import datetime
import logging
import calendar

from weasyprint import HTML

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render
from django.utils import timezone
from django.conf import settings
from django.http import (JsonResponse,
                         HttpResponseBadRequest,
                         HttpResponseNotAllowed)

from django.template.loader import render_to_string

from django.utils.dateparse import parse_datetime

from spei.models import StpTransaction
from banca.models import Transaccion, StatusTrans, SaldoReservado
from banca.serializers import DetailSerializer, EstadoSerializer
from demograficos.models import UserProfile


db_logger = logging.getLogger('db')


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) +\
        datetime.timedelta(days=4)  # this will never fail
    return (next_month - datetime.timedelta(days=next_month.day)).day


def _sum_montos(transes):
    suma = 0
    for trans in transes:
        if trans.tipoTrans.salida:
            suma -= float(trans.monto)
        else:
            suma += float(trans.monto)

    return suma


def _sum_before(trans):
    suma = 0
    date = trans.fechaValor
    user = trans.user
    transes = Transaccion.objects.filter(user=user)
    transes = transes.filter(fechaValor__lte=(date))

    suma = _sum_montos(transes)

    return suma


def _divide_trans(transes):
    trans_list = []
    sum_list = []
    sum_5 = []
    trans_5 = []
    size = len(transes)
    if size:
        new_sum = _sum_before(transes[0])

    for i in range(0, size):
        trans = transes[i]
        trans_5.append(trans)

        if i != 0:
            if trans.tipoTrans.salida:
                new_sum -= float(trans.monto)
            else:
                new_sum += float(trans.monto)

        sum_5.append(new_sum)
        moder = i % 4
        if(moder == 0 and i != 0):
            trans_list.append(trans_5)
            sum_list.append(sum_5)
            trans_5 = []
            sum_5 = []
        if(i == size - 1):
            trans_list.append(trans_5)
            sum_list.append(sum_5)

    return trans_list, sum_list


def statusStp(estado, stpId):
    if StatusTrans.objects.filter(nombre=estado):
        try:
            stpTrans = StpTransaction.objects.get(stpId=stpId)
            transaction = Transaccion.objects.get(id=stpTrans.transaccion.id)
            user_profile = UserProfile.objects.get(user=stpTrans.user)
            reservado = SaldoReservado.objects.get(
                id=stpTrans.saldoReservado.id)
            status = StatusTrans.objects.get(nombre=estado)
            if estado == "exito":
                reservado.status_saldo = "aplicado"
                reservado.fecha_aplicado_devuelto = timezone.now()
                reservado.save()

                stpTrans.stpEstado = 1
                stpTrans.save()

                transaction.fechaAplicacion = timezone.now()
                transaction.statusTrans = status
                transaction.save()
                return 1
            elif estado == "devolucion":
                reservado.status_saldo = "devuelto"
                reservado.fecha_aplicado_devuelto = timezone.now()
                reservado.save()

                stpTrans.stpEstado = 2
                stpTrans.save()

                transaction.fechaAplicacion = timezone.now()
                transaction.statusTrans = status
                transaction.save()

                user_profile.saldo_cuenta += float(reservado.saldo_reservado)
                user_profile.save()

                msg_logg = "[STP cambioestado] {} {}. Trans ID: {}".format(
                    "devolución por:",
                    reservado,
                    stpTrans.stpId)
                db_logger.info(msg_logg)
                return 2
            else:
                return 0
        except Exception as ex:
            print("ex: ", ex)

    else:
        pass


class TransactionList(generics.CreateAPIView):
    serializer_class = DetailSerializer

    def post(self, request):
        """
        Transacción recibida (sendabono)
        """

        cuenta_clabe = request.data['cuentaBeneficiario']

        try:
            profile = UserProfile.objects.get(
                cuentaClabe=cuenta_clabe)
        except Exception as ex:
            msg = "[STP sendabono] get UserProfile (ex:{}) (cta:{})".format(
                ex,
                cuenta_clabe)
            db_logger.error(msg)
            return Response({"mensaje": "devolver", "id": 1},
                            status=status.HTTP_400_BAD_REQUEST)

        if profile.cuenta_clabe_bloqueada:
            msg_logg = "{} cuenta bloqueada: {}".format(
                "[STP sendabono] (post)",
                cuenta_clabe)
            db_logger.info(msg_logg)
            return Response({"mensaje": "devolver", "id": 2},
                            status=status.HTTP_400_BAD_REQUEST)

        else:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            stp_trans = serializer.save()

            db_logger.info("[STP sendabono] (post) stpTrans creada: {}".format(
                stp_trans.id))

        return Response({"mensaje": "confirmar"})


class TransactionDetail(APIView):  # generics.CreateAPIView):
    serializer_class = EstadoSerializer

    def post(self, request):
        """
        Cambio de estado de STP hacia Cactus
        """
        _data = request.data
        db_logger.info(f"[STP cambioestado]   data: {_data}")
        print(f"[STP cambioestado]   data: {_data}")
        stpId = _data['id']
        empresa = _data['empresa']
        folioOrigen = _data['folioOrigen']
        estado = _data['estado']
        causaDevolucion = _data['causaDevolucion']
        tsLiquidacion = _data['tsLiquidacion']

        try:
            stpTrans = StpTransaction.objects.get(stpId=stpId)
            nuevo_estado = statusStp(estado, stpId)
        except Exception as ex:
            resp_msg = "recibido"
            msg = "[STP cambioestado] ERROR (get) {} {}: {}".format(
                "transacción con id ",
                stpId,
                ex)
            db_logger.error(msg)

        else:
            stpTrans.empresa = empresa
            stpTrans.folioOrigen = folioOrigen
            stpTrans.estado = estado
            stpTrans.stpEstado = nuevo_estado
            stpTrans.causaDevolucion = causaDevolucion
            stpTrans.tsLiquidacion = tsLiquidacion
            stpTrans.save()

            resp_msg = "recibido"
        respuesta = {'mensaje': resp_msg}

        return Response(respuesta)


def parse_dates_cuenta(req):
    date_from = None
    date_to = None
    is_cuenta = False

    datefrom_string = req.get("date_from", "")
    dateto_string = req.get("date_to", "")

    month_string = req.get("month", "")
    year_string = req.get("year", "")

    if (not datefrom_string or not dateto_string) \
            and (month_string and year_string):
        try:
            month = int(month_string)
            year = int(year_string)

            cuenta_month = timezone.now().month
            if month != cuenta_month:
                is_cuenta = True
        except ValueError:
            raise ValueError("Month and Year must be parsable to ints")

        date_from = timezone.datetime(year, month, 1)
        date_from = date_from.replace(
            tzinfo=timezone.get_current_timezone())
        date_to = date_from.replace(day=last_day_of_month(date_from))

    if not month_string or not year_string \
            and (datefrom_string and dateto_string):

        datefrom_string += "T00:00:00"
        dateto_string += "T00:00:00"

        date_from = parse_datetime(datefrom_string)
        date_to = parse_datetime(dateto_string)

        date_from = date_from.replace(
            tzinfo=timezone.get_current_timezone())
        date_to = date_to.replace(
            tzinfo=timezone.get_current_timezone())

    return date_from, date_to, is_cuenta


def upload_s3(file, user):
    from cactus.storage_backends import PrivateMediaStorage

    file_directory_within_bucket = 'estado_cuenta/{username}'.format(username=user.username)  # noqa:E501

    file_path = os.path.join(
        file_directory_within_bucket,
        f'cuenta_{timezone.now().strftime("%d_%s")}.pdf'
    )

    media_storage = PrivateMediaStorage()
    media_storage.save(file_path, file)
    params = {}
    params['Bucket'] = media_storage.bucket.name

    file_path = os.path.join('docs/', file_path)
    params['Key'] = file_path
    file_url = media_storage.bucket.meta.\
        client.generate_presigned_url('get_object',
            Params=params, ExpiresIn=300, HttpMethod=None)

    return file_url


def build_html_cuenta(user, date_from, date_to,
        is_cuenta, cut_off_date, month):

    transes = Transaccion.objects.filter(user=user)
    transes = transes.\
        filter(fechaValor__gte=(date_from)).\
        filter(fechaValor__lte=(date_to)).order_by('fechaValor')

    # Calculate saldos, days and get mod5 list
    trans_list, sum_list = _divide_trans(transes)
    sum_depositos = _sum_montos(transes.filter(tipoTrans__salida=False))
    sum_retiros = _sum_montos(transes.filter(tipoTrans__salida=True))

    if sum_list:
        if trans_list[0][0].tipoTrans.salida:
            saldo_initial = sum_list[0][0] + float(trans_list[0][0].monto)
        else:
            saldo_initial = sum_list[0][0] - float(trans_list[0][0].monto)
        saldo_final = sum_list[-1][-1]
    else:
        saldo_initial = saldo_final = 0

    days = (date_to - date_from).days + 1

    # Rendered
    html_string = render_to_string('banca/cuenta.html',
                                    {'trans_mod5': trans_list,
                                    'date_from': date_from,
                                    'date_to': date_to,
                                    'cut_off_date': cut_off_date,
                                    'month': month,
                                    'days': days,
                                    'sumas_mod5': sum_list,
                                    'saldo_initial': saldo_initial,
                                    'saldo_final': saldo_final,
                                    'sum_depositos': sum_depositos,
                                    'sum_retiros': sum_retiros,
                                    'is_cuenta': is_cuenta,
                                    'user': user})

    return HTML(string=html_string)


@api_view(['POST'])
def cuenta_pdf(request):
    """
    View for delivering pdf with estado cuenta from a POST

    First get the token by calling the token view. We use
    test user, ask for its password:
    curl -X POST -H 'Content-Type: application/json' \
        -i 'http://127.0.0.1:8000/api/token-auth/' \
            --data '{"username":"test", "password": ask_it}'

    Example:
    curl --header "Content-Type: application/json" \
        -H "Authorization: Token bdc56c154f7d12ed22fff72ed10d52aa1d1ec5a1" \
        --request POST  \
        --data '{"nip":"123456",
         "date_from": "2020-7-25", "date_to": "2020-8-25"}'\
        https://staging.inguz.site/api/cuenta/

    curl --header "Content-Type: application/json" \
        -H "Authorization: Basic dGVzdDp0MzV0M3I=
        Token bdc56c154f7d12ed22fff72ed10d52aa1d1ec5a1" \
        --request POST  \
        --data '{"nip":"123456",
         "month": "6", "year": "2020"}'\
        http://127.0.0.1:8000/api/cuenta/
    """
    req = request.data
    user = request.user

    """Generate pdf."""
    # Get post data
    if user.is_anonymous:
        return HttpResponseNotAllowed("Invalid credentials")

    nip_string = req.get("nip", "")

    if nip_string == "":
        return HttpResponseBadRequest("Nip must be given")

    try:
        if(not user.Uprofile.check_password(nip_string)):
            return HttpResponseNotAllowed("Incorrect NIP")
    except TypeError:
        return HttpResponseBadRequest("User has no NIP")

    parser = parse_dates_cuenta(req)

    if parser[0] is None:
        date_format_error = "Either 'month' and 'year or " + \
                    "'date_from' and 'date_to'" + \
                    " must be given"
        return HttpResponseBadRequest(date_format_error)
    else:
        date_from, date_to, is_cuenta = parser

    if (date_to.month > timezone.now().month and
            date_to.year > timezone.now().year):
        return HttpResponseBadRequest("End date cannot be more than " +
                                    "present month")

    last_day_of_month = calendar.monthrange(date_to.year, date_to.month)[1]
    fecha_dt = str(last_day_of_month) + '/' + str(date_to.month) +\
         '/' + str(date_to.year)
    cut_off_date = datetime.strptime(fecha_dt, '%d/%m/%Y')

    month_period = date_from.month
    months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
        'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    month = months[month_period - 1] + ' ' + str(date_from.year)
    # Model data
    html = build_html_cuenta(user, date_from, date_to,
        is_cuenta, cut_off_date, month)

    result = html.write_pdf()
    file = io.BytesIO(result)

    json_response = None

    if settings.USE_S3:
        file_url = upload_s3(file, user)
        json_response = JsonResponse({
            'message': 'OK',
            'fileUrl': file_url,
        })
    else:
        json = {"error": "Debug estado cuenta" +
            " not implented yet, set USE_S3 in .env to 1"}
        json_response = JsonResponse(json, status=400)

    return json_response


def my_image(request):
    return render(request, 'banca/index.html')
