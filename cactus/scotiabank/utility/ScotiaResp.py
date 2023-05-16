from spei.stpTools import randomString
from datetime import datetime, date
from django.core.exceptions import ObjectDoesNotExist
from banca.models import Transaccion, StatusTrans, TipoTransaccion
from demograficos.models import UserProfile
from scotiabank.models import (ScotiaDeposito,
                               ScotiaRetiro,
                               CatalogoCodigosTEF,
                               Archivo)
import logging


class ParserScotia:

    def FN3(nombre, contenido, resp):
        db_logger = logging.getLogger("db")
        for mov in contenido.split("\n"):
            if "SPDP" in mov:
                importe = mov[8:23]
                importe = list(importe)
                importe.insert(-2, ".")
                importe = float(''.join(importe))
                fecha = "{}/{}/{}".format(
                    mov[29:31],
                    mov[27:29],
                    mov[23:27]
                )
                clave_retiro = mov[33:53].strip()
                rfc = mov[53:66].strip()
                nombre = mov[66:106].strip()
                referencia = mov[106:122].strip()
                status = mov[323:326]
                try:
                    codigoTef = CatalogoCodigosTEF.objects.get(
                        codigo=status[1:]
                    )
                    retiro = ScotiaRetiro.objects.get(
                        referenciaPago=referencia)

                    if status == "000":
                        retiro.statusTrans = 5
                        retiro.fecha_confirmacion = datetime.strptime(
                            fecha, '%d/%m/%Y'
                        )
                        retiro.status_codigo = codigoTef
                        retiro.archivo_resumen = resp
                        retiro.save()
                        msg = "[ScotiaBank-FN3] Retiro exitoso con clave de \
                            retiro '{}' por ${} con referencia de pago '{}'. \
                            Datos del retiro [Nombre: {} / RFC: {}]".format(
                            clave_retiro,
                            importe,
                            referencia,
                            nombre,
                            rfc,
                        )
                        db_logger.info(msg)
                    else:
                        retiro.statusTrans = 8
                        retiro.fecha_confirmacion = datetime.strptime(
                            fecha, '%d/%m/%Y'
                        )
                        retiro.status_codigo = codigoTef
                        retiro.archivo_resumen = resp
                        retiro.save()
                        msg = "[ScotiaBank-FN3] Retiro no procesado con \
                            clave de retiro '{}' por ${} con referencia \
                            de pago '{}'.Código de error TEF '{}. ' \
                            Datos del retiro [Nombre: {} / RFC: {}]".format(
                            clave_retiro,
                            importe,
                            referencia,
                            codigoTef,
                            nombre,
                            rfc,
                        )
                        db_logger.warning(msg)
                except Exception as ex:
                    if CatalogoCodigosTEF.objects.filter(
                        codigo=status[1:]
                    ):
                        msg = "[ScotiaBank-error-FN3] No se encuentra \
                            transacción para la referencia de pago {} por ${}\
                            de la clave de retiro {}. \
                            Nombre: {} / RFC:{}. error: {}".format(
                            referencia,
                            importe,
                            clave_retiro,
                            nombre,
                            rfc,
                            ex
                        )
                    else:
                        msg = "[ScotiaBank-error-FN3] No se identifica el \
                            código de status {} de respuesta en el \
                            catálogoTEF para el retiro con referencia de \
                            pago  {} por ${} \
                            de la clave de retiro {}. \
                            Nombre: {} / RFC:{}. error: {}".format(
                            status,
                            referencia,
                            importe,
                            clave_retiro,
                            nombre,
                            rfc,
                            ex
                        )
                    db_logger.warning(msg)

            elif "SPDD" in mov:  # detalle devolucion
                importe = mov[8:23]
                importe = list(importe)
                importe.insert(-2, ".")
                importe = float(''.join(importe))
                fecha = "{}/{}/{}".format(
                    mov[29:31],
                    mov[27:29],
                    mov[23:27]
                )
                clave_retiro = mov[33:53].strip()
                rfc = mov[53:66].strip()
                nombre = mov[66:106].strip()
                referencia = mov[106:122].strip()
                status = mov[323:326]
                try:
                    statusTef = CatalogoCodigosTEF.objects.get(
                        codigo=status[1:])
                    retiro = ScotiaRetiro.objects.get(
                        referenciaPago=referencia)
                    retiro.statusTrans = 9
                    retiro.fecha_confirmacion = datetime.strptime(
                        fecha, '%d/%m/%Y'
                    )
                    retiro.status_codigo = statusTef
                    retiro.archivo_resumen = resp
                    retiro.save()
                    msg = "[ScotiaBank-FN3] Devolución por ${} (sin \
                        comisión) por retiro no retirado antes de su \
                        vigencia. Retiro con referencia {} por ${} con \
                        clave de retiro {}. DATOS: [ \
                        Nombre: {} / RFC:{}]".format(
                        importe,
                        referencia,
                        importe,
                        clave_retiro,
                        nombre,
                        rfc
                    )
                    db_logger.info(msg)
                except Exception as ex:
                    print(status[1:])
                    if CatalogoCodigosTEF.objects.filter(
                        codigo=status[1:]
                    ):
                        statusTef = CatalogoCodigosTEF.objects.get(
                            codigo=status[1:]
                        )
                        msg = "[ScotiaBank-error-FN3] Retiro no retirado con \
                            status {}  no tiene transacción registrada para la\
                             referencia de pago {} por ${} de la clave de \
                            retiro {}. \
                            Nombre: {} / RFC:{}. error: {}".format(
                            str(statusTef),
                            referencia,
                            importe,
                            clave_retiro,
                            nombre,
                            rfc,
                            ex
                        )
                    else:
                        msg = "[ScotiaBank-error-FN3] No se identifica el \
                            código de status '{}' de respuesta en el \
                            catálogoTEF para el retiro con referencia de pago\
                             {} por ${} de la clave de retiro {}. \
                            Nombre: {} / RFC:{}. error: {}".format(
                            status,
                            referencia,
                            importe,
                            clave_retiro,
                            nombre,
                            rfc,
                            ex
                        )
                    db_logger.warning(msg)

    def FN2(nombre, contenido, resp):
        db_logger = logging.getLogger("db")
        for mov in contenido.split("\n"):
            if "SVDA" in mov:
                importe = mov[8:23]
                importe = list(importe)
                importe.insert(-2, ".")
                importe = float(''.join(importe))
                fecha = "{}/{}/{}".format(
                    mov[29:31],
                    mov[27:29],
                    mov[23:27]
                )
                clave_retiro = mov[33:53].strip()
                rfc = mov[53:66].strip()
                nombre = mov[66:106].strip()
                referencia = mov[106:122].strip()
                status = mov[323:326]
                try:
                    codigoTef = CatalogoCodigosTEF.objects.get(
                        codigo=status[1:]
                    )
                    retiro = ScotiaRetiro.objects.get(
                        referenciaPago=referencia)

                    if status == "000":
                        retiro.statusTrans = 4
                        retiro.fecha_confirmacion = datetime.strptime(
                            fecha, '%d/%m/%Y'
                        )
                        retiro.status_codigo = codigoTef
                        retiro.archivo_respuesta_FN2 = resp
                        retiro.save()
                    else:
                        retiro.statusTrans = 8
                        retiro.fecha_confirmacion = datetime.strptime(
                            fecha, '%d/%m/%Y'
                        )
                        retiro.status_codigo = codigoTef
                        retiro.save()
                except Exception as ex:
                    if CatalogoCodigosTEF.objects.filter(
                        codigo=status[1:]
                    ):
                        msg = "[ScotiaBank-error-FN2] No se encuentra \
                            transacción para la referencia de pago {} por ${}\
                            de la clave de retiro {}. \
                            Nombre: {} / RFC:{}. error: {}".format(
                            referencia,
                            importe,
                            clave_retiro,
                            nombre,
                            rfc,
                            ex
                        )
                    else:
                        msg = "[ScotiaBank-error-FN2] No se identifica código \
                            de status {} de respuesta en el catálogoTEF para \
                            el retiro con referencia de pago {} por ${}\
                            de la clave de retiro {}. \
                            Nombre: {} / RFC:{}. error: {}".format(
                            status,
                            referencia,
                            importe,
                            clave_retiro,
                            nombre,
                            rfc,
                            ex
                        )
                    db_logger.warning(msg)

            elif "SVDR" in mov:  # detalle de rechazo
                importe = mov[8:23]
                importe = list(importe)
                importe.insert(-2, ".")
                importe = float(''.join(importe))
                fecha = "{}/{}/{}".format(
                    mov[29:31],
                    mov[27:29],
                    mov[23:27]
                )
                clave_retiro = mov[33:53].strip()
                rfc = mov[53:66].strip()
                nombre = mov[66:106].strip()
                referencia = mov[106:122].strip()
                status = mov[323:326]
                try:
                    error = CatalogoCodigosTEF.objects.get(
                        codigo=status[1:])
                    retiro = ScotiaRetiro.objects.get(
                        referenciaPago=referencia)
                    retiro.statusTrans = 8
                    retiro.archivo_respuesta_FN2 = resp
                    retiro.fecha_confirmacion = datetime.strptime(
                        fecha, '%d/%m/%Y'
                    )
                    retiro.status_codigo = error
                    retiro.save()
                except Exception as ex:
                    if CatalogoCodigosTEF.objects.filter(
                        codigo=status[1:]
                    ):
                        error = CatalogoCodigosTEF.objects.get(
                            codigo=status[1:]
                        )
                        msg = "[ScotiaBank-error-FN2] Retiro con error {}  no \
                            tiene transacción registrada para la \
                            referencia de pago {} por ${} de la clave de \
                            retiro {}. \
                            Nombre: {} / RFC:{}. error: {}".format(
                            str(error),
                            referencia,
                            importe,
                            clave_retiro,
                            nombre,
                            rfc,
                            ex
                        )
                    else:
                        msg = "[ScotiaBank-error-FN2] No se identifica código \
                            de status '{}' de respuesta en el catálogoTEF para\
                             el retiro con referencia de pago {} por ${}\
                            de la clave de retiro {}. \
                            Nombre: {} / RFC:{}. error: {}".format(
                            status,
                            referencia,
                            importe,
                            clave_retiro,
                            nombre,
                            rfc,
                            ex
                        )
                    db_logger.warning(msg)

    def FN5(nombre, contenido, resp):
        db_logger = logging.getLogger('db')
        lineas = []
        linea = 0
        error = False
        for mov in contenido.split("\n"):
            linea += 1
            lineas.append(mov)
            if "ERROR" in mov:
                linea_error = linea
                error = True
        nombre_archivo = (lineas[0])[108:172].strip()
        num_archivos = int((lineas[3])[34:36].strip())
        try:
            archivo = Archivo.objects.get(
                nombre=nombre_archivo
            )
            retiros = ScotiaRetiro.objects.filter(
                archivo=archivo
            )
            if error is False:
                archivo.status = 1
                archivo.respuesta_FN5 = resp
                archivo.save()
                for retiro in retiros:
                    retiro.statusTrans = 2
                    retiro.save()
            else:
                errorMsg = (lineas[linea_error - 1])[34:].strip()
                archivo.status = 2
                archivo.respuesta_FN5 = resp
                archivo.save()
                for retiro in retiros:
                    retiro.statusTrans = 7
                    retiro.rechazoMsg = errorMsg
                    retiro.save()
                msg = "[ScotiaBank-error-FN5] El Archivo '{}' fue \
                    rechazado con el error '{}'. Scotiabank lleva {} archivos \
                    registrados en el día.".format(
                    nombre_archivo,
                    errorMsg,
                    num_archivos)
                db_logger.warning(msg)
        except Exception as ex:
            msg = "[ScotiaBank-error-FN5] El Archivo de respuesta '{}' de SB \
                sobre el archivo enviado '{}' no tiene un archivo o \
                movimientos de retiro asociados en la \
                base de datos. Error: '{}'".format(
                resp.nombre_archivo,
                nombre_archivo,
                ex)
            db_logger.warning(msg)

    def H34(nombre, contenido):
        pass

    def H83(nombre, contenido):
        pass

    def H93(nombre, contenido, resp):
        db_logger = logging.getLogger('db')
        for mov in contenido.split("\n")[1:-2]:
            datos = mov.split("|")
            nombre_plaza = datos[2].strip()
            num_plaza = datos[3].strip()
            num_sucursal = datos[4].strip()
            fecha_recibo = datos[5].strip()
            fecha_pago = datos[6].strip()
            fecha_deposito = datos[7].strip()
            importe = (datos[9].strip()).replace("$", "")
            forma_pago = datos[10].strip()
            hora_pago = datos[14]
            referencia = datos[16].strip()
            fl = datos[17].strip()
            fecha_limite = "{}/{}/{}".format(fl[-2:], fl[4:6], fl[:4])
            try:
                trans = ScotiaDeposito.objects.get(
                    referencia_cobranza=str(referencia))
                if trans.statusTrans != 2:
                    trans.statusTrans = 2
                    trans.archivo_respuesta_H93 = resp
                    trans.nombre_plaza_origen = nombre_plaza
                    trans.num_plaza_cobro = num_plaza
                    trans.num_sucursal_cobro = num_sucursal
                    trans.fecha_presentacion_pago = datetime.strptime(
                        fecha_recibo, '%d/%m/%Y'
                    )
                    trans.fecha_captura_contable = datetime.strptime(
                        fecha_pago, '%d/%m/%Y'
                    )
                    trans.fecha_aplicacion_recursos = datetime.strptime(
                        fecha_deposito, '%d/%m/%Y'
                    )
                    trans.importe_documento = float(importe)
                    trans.indicador_forma_pago = forma_pago
                    trans.hora_recepcion_pago = datetime.strptime(
                        hora_pago, '%H:%M'
                    )
                    trans.fecha_limite = datetime.strptime(
                        fecha_limite, '%d/%m/%Y'
                    )
                    trans.save()
                    clabe = referencia[:18]
                    msg = "[ScotiaBank-H93] Depósito scotiabank recibido con \
                        referencia {} por ${} a la cuenta {}".format(
                        referencia,
                        importe,
                        clabe)
                    db_logger.info(msg)
            except ObjectDoesNotExist as ex:
                validaClabe = referencia[:18]
                if UserProfile.objects.filter(cuentaClabe=validaClabe):
                    user_profile = UserProfile.objects.get(
                        cuentaClabe=validaClabe)
                    fecha = datetime.now().strftime(
                        '%Y-%m-%d %H:%M:%S')
                    status = StatusTrans.objects.get(
                        nombre="exito")
                    tipo = TipoTransaccion.objects.get(codigo=3)
                    claveR = randomString()
                    comision = 0
                    main_trans = Transaccion.objects.create(
                        user=user_profile.user,
                        fechaValor=fecha,
                        monto=float(importe),
                        statusTrans=status,
                        tipoTrans=tipo,
                        concepto="Depósito Cliente",
                        claveRastreo=claveR
                    )
                    ScotiaDeposito.objects.create(
                        statusTrans=2,
                        nombre_plaza_origen=nombre_plaza,
                        num_plaza_cobro=num_plaza,
                        num_sucursal_cobro=num_sucursal,
                        fecha_presentacion_pago=datetime.strptime(
                            fecha_recibo, '%d/%m/%Y'
                        ),
                        fecha_captura_contable=datetime.strptime(
                            fecha_pago, '%d/%m/%Y'
                        ),
                        fecha_aplicacion_recursos=datetime.strptime(
                            fecha_deposito, '%d/%m/%Y'
                        ),
                        indicador_forma_pago=forma_pago,
                        hora_recepcion_pago=datetime.strptime(
                            hora_pago, '%H:%M'
                        ),
                        fecha_limite=datetime.strptime(
                            fecha_limite, '%d/%m/%Y'
                        ),
                        ordenante=user_profile.user,
                        importe_documento=float(importe),
                        comision=comision,
                        referencia_cobranza=referencia,
                        fecha_inicial=date.today(),
                        ubicacion=nombre_plaza,
                        transaccion=main_trans,
                        archivo_respuesta_H93=resp
                    )
                    user_profile.saldo_cuenta += float(importe) - comision
                    user_profile.save()
                    msg = "[ScotiaBank-error-H93] No hay transacción para \
                        el depósito ScotiaBank con referencia {} por ${}. \
                        Depósito no reconocido. CLABE {} reconocida, saldo \
                        sin comision depositados a la cuenta.".format(
                        referencia,
                        importe,
                        validaClabe)
                    db_logger.warning(msg)
                else:
                    msg = "[ScotiaBank-error-H93] No hay transacción para el \
                        depósito ScotiaBank con  referencia {} por ${}. Clabe\
                         y transacción no reconocidas. error: {}".format(
                        referencia,
                        importe,
                        ex)
                    db_logger.warning(msg)

    def FN12(nombre, contenido):
        pass
