import os
import io
import datetime
import logging
import calendar

from weasyprint import HTML

from rest_framework import generics, renderers
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render
from django.utils import timezone
from django.conf import settings
from django.http import (JsonResponse,
                         HttpResponse,
                         HttpResponseBadRequest,
                         HttpResponseNotAllowed,)
#  FileResponse

from django.template.loader import render_to_string

from spei.models import StpTransaction
from banca.models import Transaccion, StatusTrans, SaldoReservado
from banca.utils.comprobantesPng import CompTrans
from spei.stpTools import randomString
from banca.serializers import DetailSerializer, EstadoSerializer
from banca.utils.limiteTrans import LimiteTrans
from demograficos.models import UserProfile


trans_entrada = [1, 3, 8, 11, 12, 15, 19, 21]

db_logger = logging.getLogger('db')


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) +\
        datetime.timedelta(days=4)  # this will never fail
    return (next_month - datetime.timedelta(days=next_month.day)).day


def _sum_montos(transes):
    suma = 0
    for trans in transes:
        if int(trans.tipoTrans.codigo) in trans_entrada:
            suma += float("{:.2f}".format(trans.monto))
        else:
            suma -= float("{:.2f}".format(trans.monto))

    return round(suma, 2)


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
            if int(trans.tipoTrans.codigo) in trans_entrada:
                new_sum += float(trans.monto)
            else:
                new_sum -= float(trans.monto)
        sum_5.append(new_sum)
        moder = i % 4
        if moder == 0 and i != 0:
            trans_list.append(trans_5)
            sum_list.append(sum_5)
            trans_5 = []
            sum_5 = []
        if i == size - 1:
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

                user_profile.saldo_cuenta += float(
                    "{:.2f}".format(reservado.saldo_reservado))
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
        try:
            cuenta_clabe = request.data['cuentaBeneficiario']
            monto = float(request.data['monto'])
            referencia = request.data['referenciaNumerica']
            concepto = request.data['conceptoPago']
            ordenante = request.data['institucionOrdenante']
            claveRastreo = request.data['claveRastreo']
            cuentaOrdenante = request.data['cuentaOrdenante']
            fechaOperacion = request.data['fechaOperacion']
        except Exception as ex:
            msg = f"[STP post sendabono]:{ex}"
            db_logger.error(msg)

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

        valida_limite = LimiteTrans(profile.user.id)

        if profile.cuenta_clabe_bloqueada:
            msg_logg = "{} cuenta bloqueada: {}".format(
                "[STP sendabono] (post)",
                cuenta_clabe)
            db_logger.info(msg_logg)
            return Response({"mensaje": "devolver", "id": 2},
                            status=status.HTTP_400_BAD_REQUEST)

        elif not valida_limite.saldo_max(monto) or \
                not valida_limite.trans_mes(monto):
            try:
                status_trans = StatusTrans.objects.get(nombre="devolucion")
                tipo = TipoTransaccion.objects.get(codigo=1)
                claveR = claveRastreo
                causa = "Límte transaccional superado"
                trans = Transaccion.objects.create(
                    user=profile.user,
                    fechaValor=timezone.now(),
                    fechaAplicacion=timezone.now(),
                    monto=float(monto),
                    statusTrans=status_trans,
                    tipoTrans=tipo,
                    concepto=concepto,
                    claveRastreo=randomString()
                )
                StpTransaction.objects.create(
                    user=profile.user,
                    nombre=profile.get_nombre_completo(),
                    monto=float(monto),
                    banco=ordenante,
                    clabe=cuenta_clabe,
                    concepto=concepto,
                    referencia=referencia,
                    claveRastreo=claveR,
                    nombreBeneficiario=profile.get_nombre_completo(),
                    fechaOperacion=fechaOperacion,
                    cuentaOrdenante=cuentaOrdenante,
                    referenciaNumerica=referencia,
                    conceptoPago=concepto,
                    cuentaBeneficiario=cuenta_clabe,
                    transaccion=trans,
                    causaDevolucion=causa,
                    stpEstado=2,
                    rechazada=True,
                    RechazadaMsj=causa
                )
                msg_logg = "{} {}: {}".format(
                    "[STP sendabono] (post)",
                    causa,
                    cuenta_clabe)
                db_logger.info(msg_logg)
            except Exception as ex:
                msg_logg = f"[STP sendabono devolución]: {profile.user}: {ex}"
                db_logger.error(msg_logg)
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
    is_cuenta = False

    month = req.get("month")
    year = req.get("year")

    if month:
        try:
            cuenta_month = month
            year = year

            if month != cuenta_month:
                is_cuenta = True
        except ValueError:
            raise ValueError("Month and Year must be parsable to ints")

        date_from = timezone.datetime(day=1, month=month, year=year)
        date_to = date_from.replace(day=last_day_of_month(date_from))

    if not month:

        date_from = date_from.replace(
            tzinfo=timezone.get_current_timezone())
        date_to = date_to.replace(
            tzinfo=timezone.get_current_timezone())

    return date_from, date_to, is_cuenta


def upload_s3(file, user):
    print("------")
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
        client.generate_presigned_url(
            'get_object',
            Params=params, ExpiresIn=300, HttpMethod=None)

    return file_url


def build_html_cuenta(user, date_from, date_to,
                      is_cuenta, cut_off_date, month):

    date_to = date_to + datetime.timedelta(hours=23, minutes=59, seconds=59)

    transes = Transaccion.objects.filter(user=user)
    transes = transes.\
        filter(fechaValor__gte=(date_from)).\
        filter(fechaValor__lte=(date_to)).order_by('fechaValor')
    trans_list = [transes[i:i + 4] for i in range(0, len(transes), 4)]
    filter_retiros_mes = []
    filter_depositos_mes = []
    for trans in transes:
        if int(trans.tipoTrans.codigo) in trans_entrada:
            filter_depositos_mes.append(trans)
        else:
            filter_retiros_mes.append(trans)

    sum_depositos = _sum_montos(filter_depositos_mes)
    sum_retiros = _sum_montos(filter_retiros_mes)
    sum_depositos = "{:.2f}".format(sum_depositos)
    sum_retiros = "{:.2f}".format(sum_retiros)
    days = (date_to - date_from).days + 1

    hoy = timezone.now()
    transesTotales = Transaccion.objects.filter(user=user)
    transesTotales = transesTotales.\
        filter(fechaValor__gte=(date_from)).\
        filter(fechaValor__lte=(hoy)).order_by('fechaValor')
    saldo_actual = UserProfile.objects.filter(user=user).first().saldo_cuenta
    saldo_inicial = saldo_actual
    for trans in transesTotales:
        if int(trans.tipoTrans.codigo) in trans_entrada:
            saldo_inicial -= float(trans.monto)
        else:
            saldo_inicial += float(trans.monto)
    saldo_final = saldo_inicial

    sum_list = []
    for trans in transes:
        if int(trans.tipoTrans.codigo) in trans_entrada:
            saldo_final += float(trans.monto)
        else:
            saldo_final -= float(trans.monto)
        sum_list.append(saldo_final)
    sum_list = [sum_list[i:i + 4] for i in range(0, len(sum_list), 4)]
    saldo_inicial = "{:.2f}".format(round(saldo_inicial))
    saldo_final = "{:.2f}".format(round(saldo_final))

    # Rendered
    html_string = render_to_string(
        'banca/cuenta.html',
        {'trans_mod5': trans_list,
         'date_from': date_from,
         'date_to': date_to,
         'cut_off_date': cut_off_date,
         'month': month,
         'days': days,
         'sumas_mod5': sum_list,
         'saldo_initial': saldo_inicial,
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
        if not user.Uprofile.check_password(nip_string):
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


class CustomRenderer(renderers.BaseRenderer):
    media_type = 'image/png'
    format = 'png'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


@api_view(['GET'])
def comprobante_trans(request, trans_id):

    # req = request.data
    # trans_id = req.get("trans_id", "")
    # trans_id = request.GET["trans_id"]
    user = request.user
    trans = None
    trans = Transaccion.objects.get(pk=trans_id)
    # print(trans)
    print("rielrielriel")
    print(trans.tipoTrans)
    comp = CompTrans(trans)
    comp_file = comp.trans()
    print(type(comp_file))
    if settings.USE_S3:

        file_url = upload_s3(comp_file, user)

        json_response = JsonResponse({
            'message': 'OK',
            'fileUrl': file_url,
        })
    else:
        print("sadfsafasdfsadfadsf")
        # json = {"error": "Debug estado cuenta" +
        #         " not implented yet, set USE_S3 in .env to 1"}
        # json_response = JsonResponse(json, status=400)

        return HttpResponse(comp_file, content_type="image/jpg")

    return json_response


def my_image(request):
    return render(request, 'banca/index.html')
