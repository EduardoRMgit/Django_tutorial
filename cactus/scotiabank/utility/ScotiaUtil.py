import io

from weasyprint import HTML

from datetime import datetime, timedelta, time

from django.template.loader import render_to_string
from django.utils import timezone
from django.core.files.base import ContentFile

from spei.models import InstitutionBanjico

from scotiabank.models import Archivo

from scotiabank.utility.utcToLocal import utc_to_local

import logging


def GeneraRetiro(movimientos):

    db_logger = logging.getLogger("db")
    hoy = timezone.now()
    dias_delta = (hoy.day) != ((
        hoy - timedelta(hours=22)).day) - 0
    rango_inicio = (hoy - timedelta(days=dias_delta)).replace(
        hour=22, minute=0, second=0, microsecond=0)
    secuencia = Archivo.objects.filter(
        fecha__range=[rango_inicio, hoy],
        tipo_archivo="Retiro").count() + 1
    secuencia_archivo = Archivo.objects.filter(
        fecha__year=hoy.year,
        fecha__month=hoy.month,
        fecha__day=hoy.day,
        tipo_archivo="Retiro").count() + 1
    try:
        fecha_t = hoy.strftime("%Y%m%d")
        numero_convenio = "17244"
        referencia_empresa = "1702"
        cuenta_cargo = '25600126235'

        name = "H2HJDF000000{}001{}{}.1001007FN100{}.txt".format(
            '{:0>5}'.format(referencia_empresa),
            '{:0>8}'.format(numero_convenio),
            fecha_t,
            '{:0>3}'.format(str(secuencia_archivo)))

        cont_head1 = "EEHA{}{}000000000000000000000000000{}".format(
            '{:0>5}'.format(numero_convenio),
            '{:0>2}'.format(str(secuencia)),
            " " * 332)
        cont_head2 = "EEHB000000{}00000{}000{}".format(
            cuenta_cargo,
            '{:0>5}'.format(referencia_empresa),
            " " * 336)

        generado = Archivo.objects.create(
            nombre=name,
            secuencia=secuencia,
            tipo_archivo="Retiro"
        )

        contenido_ = "{}\n{}\n".format(
            cont_head1,
            cont_head2
        )

        for mov in movimientos:
            usuario = mov.ordenante.Uprofile
            monto = float(mov.monto)
            forma_pago = "01"
            moneda_pago = "00"
            servicio_concepto = mov.servicio_concepto
            banco_emisor = "044"
            tipo_cuenta_ordenante = mov.tipoCuentaOrdenante
            referenciaPago = str(fecha_t) + "{}".format(
                '{:0>8}'.format(mov.transaccion.id),
            )
            banco_ordenante = "044"
            cuenta_ordenante = "11111111111"
            clave_ordenante = ''
            dias_vigencia = "001"
            for digito in usuario.cuentaClabe:
                if digito != "0":
                    clave_ordenante += digito
            rfc = usuario.rfc
            email = mov.ordenante.email
            if rfc is None:
                rfc = ''
            else:
                rfc = usuario.rfc
            nombre = (str(mov.ordenante.get_full_name()) + " " + str(
                usuario.apMaterno))
            if len(email) > 0:
                DM = '\nEEDM{}'.format(
                    '{:<100}'.format(email),
                )
            else:
                DM = ""
            if len(nombre) > 0:
                lin = "EEDA{}{}{}{}{}{}{}{}{}{}{}{}{}{} {}{}{}{}{}{}{}{}\n".format(  # noqa: E501
                    '{:<2}'.format(forma_pago),
                    '{:<2}'.format(moneda_pago),
                    '{:0>16}'.format('%.2f' % monto).replace('.', ''),
                    fecha_t,
                    '{:<2}'.format(servicio_concepto),
                    '{:<20}'.format(clave_ordenante),
                    '{:<13}'.format(rfc),
                    '{:<40}'.format(nombre.upper()),
                    '{:0>16}'.format(str(referenciaPago)),
                    '0' * 10,
                    '{:0>20}'.format(str(cuenta_ordenante)),
                    '0' * 5,
                    ' ' * 40,
                    str(tipo_cuenta_ordenante),
                    '00000',
                    '{}{}'.format(banco_emisor, banco_ordenante),
                    '{}'.format(dias_vigencia),
                    '{:<50}'.format(mov.conceptoPago),
                    ' ' * 60,
                    '0' * 25,
                    ' ' * 22,
                    '{:<105}'.format(DM),
                )
                mov.statusTrans = 1
                mov.clave_retiro = clave_ordenante
                mov.referenciaPago = str(referenciaPago)
                mov.vigencia = hoy.date()
                mov.save()
            else:
                raise Exception("No puede tener los campos vacios")
            contenido_ += lin
        num_movimientos = movimientos.count()
        importe_total = sum(
            list(
                map(
                    lambda m: float(m.monto), movimientos
                )
            )
        )
        t_num_mov = '{:0>7}'.format(str(num_movimientos))
        t_imp_t = ('{:0>18}'.format('%.2f' %
                                    importe_total)).replace('.', '')
        cont_tail1 = "EETB{}{}{}{}".format(t_num_mov,
                                           t_imp_t,
                                           "0" * 219,
                                           " " * 123)
        cont_tail2 = "EETA{}{}{}{}".format(t_num_mov,
                                           t_imp_t,
                                           "0" * 219,
                                           " " * 123)

        contenido_ += "{}\n{}\n".format(
            cont_tail1,
            cont_tail2
        )
        generado.txt.save(name, ContentFile(contenido_.encode('latin1')))
        generado.contenido_archivo = contenido_
        generado.save()
        for m in movimientos:
            m.archivo = generado
            m.save()

        mensaje = "Archivo generado: {}".format(generado.nombre)
    except Exception as ex:
        msg = "[ScotiaBank-Error] No fue posible generar el archivo: {} \
            de Retiro. Error: {}".format(
            name,
            ex
        )
        db_logger.error(msg)
        mensaje = "No fue posible generar el archivo: {}".format(ex)

    return mensaje


def GeneraTransferencia(movimientos):

    db_logger = logging.getLogger("db")
    hoy = timezone.now()
    dias_delta = (hoy.day) != ((
        hoy - timedelta(hours=17)).day) - 0
    rango_inicio = (hoy - timedelta(days=dias_delta)).replace(
        hour=17, minute=0, second=0, microsecond=0)
    secuencia = Archivo.objects.filter(
        fecha__range=[rango_inicio, hoy],
        tipo_archivo="Transferencia").count() + 1
    secuencia_archivo = Archivo.objects.filter(
        fecha__year=hoy.year,
        fecha__month=hoy.month,
        fecha__day=hoy.day,
        tipo_archivo="Transferencia").count() + 1

    if hoy.weekday(
    ) in range(0, 5) and timezone.now().time() <= time(16, 49, 54):
        fecha_t = hoy
    elif hoy.weekday(
    ) in range(0, 4) and timezone.now().time() >= time(16, 49, 55):
        fecha_t = hoy + timedelta(1)
    elif (hoy.weekday() == 4 and timezone.now().time(
    ) >= time(16, 49, 55)) or (hoy.weekday() in range(5, 7)):
        dias_delta = -hoy.weekday() + 7
        fecha_t = hoy + timedelta(dias_delta)
    else:
        fecha_t = datetime(1999, 12, 31)
    try:
        fecha_t = fecha_t.strftime("%Y%m%d")
        numero_convenio = '7640'
        referencia_empresa = "1702"
        dias_vigencia = '001'
        cuenta_cargo = '25600126235'

        name = "H2HJDF000000{}001{}{}.1001007FN100{}.txt".format(
            '{:0>5}'.format(referencia_empresa),
            '{:0>8}'.format(numero_convenio),
            fecha_t,
            '{:0>3}'.format(str(secuencia_archivo)))

        cont_head1 = "EEHA{}{}000000000000000000000000000{}".format(
            '{:0>5}'.format(numero_convenio),
            '{:0>2}'.format(str(secuencia)),
            " " * 332)
        cont_head2 = "EEHB000000{}00000{}000{}".format(
            cuenta_cargo,
            '{:0>5}'.format(referencia_empresa),
            " " * 336)

        generado = Archivo.objects.create(
            nombre=name,
            secuencia=secuencia,
            tipo_archivo="Transferencia"
        )

        contenido_ = "{}\n{}\n".format(
            cont_head1,
            cont_head2
        )

        for mov in movimientos:
            forma_pago = "04"
            moneda_pago = "00"
            servicio_concepto = mov.servicio_concepto
            banco_emisor = "044"
            tipo_cuenta_beneficiario = mov.tipoCuentaBeneficiario
            referenciaPago = str(fecha_t) + "{}".format(
                '{:0>8}'.format(mov.id),
            )
            institucion_id = InstitutionBanjico.objects.filter(
                short_name=mov.institucionBeneficiariaInt)
            banco_beneficiario = institucion_id.first().short_id
            cuenta_beneficiario = mov.cuentaBeneficiario
            clave_beneficiario = mov.clave_beneficiario
            if (mov.rfcCurpBeneficiario) is None:
                rfc_beneficiario = ''
            elif len(mov.rfcCurpBeneficiario) == 13:
                rfc_beneficiario = mov.rfcCurpBeneficiario
            else:
                rfc_beneficiario = ''
            if mov.ordenante.email is None:
                detalle_mail = ''
            else:
                detalle_mail = mov.ordenante.email
            DM = '\nEEDM{}'.format(
                '{:<100}'.format(detalle_mail),
            )
            lin = "EEDA{}{}{}{}{}{}{}{}{}{}{}{}{}{} {}{}{}{}{}{}{}{}\n".format(  # noqa: E501
                '{:<2}'.format(forma_pago),
                '{:<2}'.format(moneda_pago),
                '{:0>16}'.format('%.2f' % float(
                    mov.monto)).replace('.', ''),
                fecha_t,
                '{:<2}'.format(servicio_concepto),
                '{:<20}'.format(clave_beneficiario),
                '{:<13}'.format(rfc_beneficiario),
                '{:<40}'.format(mov.nombreBeneficiario),
                '{:0>16}'.format(str(referenciaPago)),
                '0' * 10,
                '{:0>20}'.format(str(cuenta_beneficiario)),
                '0' * 5,
                ' ' * 40,
                str(tipo_cuenta_beneficiario),
                '00000',
                '{}{}'.format(banco_emisor, banco_beneficiario),
                '{}'.format(dias_vigencia),
                '{:<50}'.format(mov.conceptoPago),
                ' ' * 60,
                '0' * 25,
                ' ' * 22,
                '{:<105}'.format(DM),
            )
            contenido_ += lin
            mov.statusTrans = 1
            mov.save()

        num_movimientos = movimientos.count()
        importe_total = sum(
            list(
                map(
                    lambda m: float(m.monto), movimientos
                )
            )
        )
        t_num_mov = '{:0>7}'.format(str(num_movimientos))
        t_imp_t = ('{:0>18}'.format('%.2f' %
                                    importe_total)).replace('.', '')
        cont_tail1 = "EETB{}{}{}{}".format(t_num_mov,
                                           t_imp_t,
                                           "0" * 219,
                                           " " * 123)
        cont_tail2 = "EETA{}{}{}{}".format(t_num_mov,
                                           t_imp_t,
                                           "0" * 219,
                                           " " * 123)

        contenido_ += "{}\n{}\n".format(
            cont_tail1,
            cont_tail2
        )
        generado.txt.save(name, ContentFile(contenido_.encode('latin1')))
        generado.contenido_archivo = contenido_
        generado.save()
        for m in movimientos:
            m.archivo = generado
            m.save()

        mensaje = "Archivo generado: {}".format(generado.nombre)
    except Exception as ex:
        msg = "[ScotiaBank-Error] No fue posible generar el archivo: {} \
            de Transferencia. Error: {}".format(
            name,
            ex
        )
        db_logger.error(msg)
        mensaje = "No fue posible generar el archivo: {}".format(ex)

    return mensaje


def genera_pdf(instance, datosFijos):
    convenio = str(datosFijos.numero_empresa)
    empresa = str(datosFijos.nombre_empresa)
    tipo = str(datosFijos.tipo_transaccion)
    fecha_hora_solicitud = utc_to_local(instance.time).strftime(
        "%d/%m/%y %H:%M:%S")
    fecha_t = utc_to_local(instance.time).strftime("%Y%m%d")
    if datosFijos.tipo_transaccion == "Deposito":
        ref = str(instance.referencia_cobranza)
        importe = str(round((
            instance.importe_documento), 2))
        transaccion = str(fecha_t) + "{}".format(
            '{:0>8}'.format(instance.transaccion.id)
        )
    elif datosFijos.tipo_transaccion == "Retiro":
        ref = str(instance.clave_retiro)
        importe = str(round(instance.monto, 2))
        transaccion = str(instance.referenciaPago)
    instruccion = str(datosFijos.instrucciones)
    if instruccion is None:
        instruccion = ""
    nombre = str(instance.ordenante.first_name)
    apellidos = str(
        instance.ordenante.last_name) + str(
            instance.ordenante.Uprofile.apMaterno)
    if instance.fecha_limite is None or instance.fecha_limite == "":
        vigencia = utc_to_local(timezone.now()).date(
        ).strftime("%d-%m-%Y")
    else:
        vigencia = instance.fecha_limite.strftime(
            "%d-%m-%Y"
        )
    nombre_archivo = str(ref) + str(
        importe).replace(".", "") + transaccion + ".pdf"
    html_string = render_to_string(
        'scotiabanck/comprobante.html',
        {
            'empresa': empresa,
            'titulo': tipo,
            'convenio': convenio,
            'user.first_name': nombre,
            'user.last_name': apellidos,
            'referencia': ref,
            'importe': ("$" + importe),
            'vigencia': vigencia,
            'transaccion': transaccion,
            'date_to': fecha_hora_solicitud})
    html = HTML(string=html_string)
    result = html.write_pdf()
    file = io.BytesIO(result)
    return file, nombre_archivo
