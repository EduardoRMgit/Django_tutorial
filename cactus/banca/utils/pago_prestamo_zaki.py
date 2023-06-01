import logging

from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User

from spei.stpTools import randomString
from banca.models import (StatusTrans, TipoTransaccion,
                          Transaccion, PrestamoZakiTransaccion,
                          PagoZakiTransaccion)


db_logger = logging.getLogger('db')


def crear_prestamo(request):
    # Permissions: Sólo permitida al usuario Zaki
    # {"username": "5529641640", "amount": 13.00}
    # {"username": "5573973545", "amount": 500.00}
    username = request['username']
    abono = request['amount']

    try:
        ordenante = User.objects.get(username=settings.USERNAME_ZAKI)
    except Exception as ex:
        db_logger.warning(
            f"[ZAKI crear_prestamo] Usuario Zaki no encontrado. ex: {ex}")
        return {
            'error': -24710,
            # 'msg': "Usuario Zaki no encontrado",
        }

    if float(abono) > ordenante.Uprofile.saldo_cuenta:
        db_logger.warning("[ZAKI crear_prestamo] Saldo Zaki insuficiente")
        return {
            'error': -24711,
            # 'msg': "Saldo Zaki insuficiente",
        }

    user_beneficiario = User.objects.filter(
        username=username,
        is_active=True)
    if user_beneficiario.count() == 0:
        db_logger.warning(
            f"[ZAKI crear_prestamo] User {username} no encontrado o inactivo.")
        return {
            'error': -24712,
            # 'msg': "Usuario no encontrado",
        }
    user_beneficiario = user_beneficiario.last()

    prestamos = user_beneficiario.prestamos_zaki.all()
    num_prestamos = prestamos.filter(status="P").count()
    if num_prestamos > 0:
        db_logger.warning(
            f"[ZAKI crear_prestamo] User {username} ya cuenta con préstamo.")
        return {
            'error': -24714,
            # 'msg': "Usuario no encontrado",
        }

    fecha = datetime.now()
    status = StatusTrans.objects.get(nombre="exito")
    tipo_enviada = TipoTransaccion.objects.get(codigo=200)  # Prestamo enviada
    tipo_recibida = TipoTransaccion.objects.get(
        codigo=201)  # Prestamo recibida
    claveR = randomString()
    monto2F = "{:.2f}".format(round(float(abono), 2))

    enviada_trans = Transaccion.objects.create(
        user=ordenante,
        fechaValor=fecha,
        fechaAplicacion=fecha,
        monto=float(abono),
        statusTrans=status,
        tipoTrans=tipo_enviada,
        concepto="Préstamo Zaki",
        claveRastreo=claveR
    )
    recibida_trans = Transaccion.objects.create(
        user=user_beneficiario,
        fechaValor=fecha,
        fechaAplicacion=fecha,
        monto=float(abono),
        statusTrans=status,
        tipoTrans=tipo_recibida,
        concepto="Préstamo Zaki",
        claveRastreo=claveR
    )
    PrestamoZakiTransaccion.objects.create(
        user=user_beneficiario,
        fechaOperacion=fecha,
        enviada_prestamo=enviada_trans,
        recibida_prestamo=recibida_trans,
        monto=monto2F,
        status="P"
    )

    # Hacerlos atómicos (en general desde antes de los creates)
    # if_check_abono_>_saldo:
    ordenante.Uprofile.saldo_cuenta -= round(float(abono), 2)
    ordenante.Uprofile.save()
    user_beneficiario.Uprofile.saldo_cuenta += round(float(abono), 2)
    user_beneficiario.Uprofile.save()
    # else_check: warning and raise

    msg = "[Zaki crear_prestamo] Exitoso para el usuario: {} por {}".format(
        username,
        abono)
    db_logger.info(msg)

    return {
        "created": True
    }


def liquidar_prestamo(request):
    # Permissions: Sólo permitida al usuario Zaki
    # {"username": "5529641640"}
    username = request['username']

    try:
        user_zaki = User.objects.get(username=settings.USERNAME_ZAKI)
    except Exception as ex:
        db_logger.warning(
            f"[ZAKI liquidar_prestamo] Usuario Zaki no encontrado. ex: {ex}")
        return {
            'error': -24713,
            # 'msg': "Usuario Zaki no encontrado",
        }

    ordenante = User.objects.filter(
        username=username,
        is_active=True)
    if ordenante.count() == 0:
        db_logger.warning(
            f"[ZAKI liquidar_prest] User {username} no encontrado o inactivo.")
        return {
            'error': -24715,
            # 'msg': "Usuario no encontrado",
        }
    ordenante = ordenante.last()
    prestamos = ordenante.prestamos_zaki.all()
    num_prestamos = prestamos.filter(status="P").count()
    if num_prestamos == 0:
        db_logger.warning(
            f"[ZAKI liquidar_prestamo] User {username} sin préstamo activo.")
        return {
            'error': -24716,
            # 'msg': "Usuario sin préstamos",
        }

    if num_prestamos > 1:
        db_logger.warning(
            f"[ZAKI liquidar_presta] User {username} con múltiples préstamos.")
        return {
            'error': -24717,
            # 'msg': "Usuario con múltiples préstamos",
        }

    prestamo = prestamos.get(status="P")
    abono = prestamo.monto
    if float(abono) > ordenante.Uprofile.saldo_cuenta:
        db_logger.warning(
            "[ZAKI liquidar_prestamo] Saldo Usuario insuficiente")
        return {
            'error': -24718,
            # 'msg': "Saldo Usuario insuficiente",
        }

    fecha = datetime.now()
    status = StatusTrans.objects.get(nombre="exito")
    tipo_enviada = TipoTransaccion.objects.get(codigo=202)  # Pago enviada
    tipo_recibida = TipoTransaccion.objects.get(
        codigo=203)  # Pago recibida
    claveR = randomString()
    monto2F = "{:.2f}".format(round(float(abono), 2))

    enviada_trans = Transaccion.objects.create(
        user=ordenante,
        fechaValor=fecha,
        fechaAplicacion=fecha,
        monto=float(abono),
        statusTrans=status,
        tipoTrans=tipo_enviada,
        concepto="Pago Zaki",
        claveRastreo=claveR
    )
    recibida_trans = Transaccion.objects.create(
        user=user_zaki,
        fechaValor=fecha,
        fechaAplicacion=fecha,
        monto=float(abono),
        statusTrans=status,
        tipoTrans=tipo_recibida,
        concepto="Pago Zaki",
        claveRastreo=claveR
    )
    PagoZakiTransaccion.objects.create(
        user=ordenante,
        fechaOperacion=fecha,
        enviada_pago=enviada_trans,
        recibida_pago=recibida_trans,
        monto=monto2F
    )

    # Hacerlos atómicos (en general desde antes de los creates)
    # if_check_abono_>_saldo:
    ordenante.Uprofile.saldo_cuenta -= round(float(abono), 2)
    ordenante.Uprofile.save()
    user_zaki.Uprofile.saldo_cuenta += round(float(abono), 2)
    user_zaki.Uprofile.save()
    prestamo.status = "L"
    prestamo.save()
    # else_check: warning and raise

    msg = "[Zaki liquidar_prestamo] Exitoso para el usuario: {} por {}".format(
        username,
        abono)
    db_logger.info(msg)

    return {
        "created": True
    }
