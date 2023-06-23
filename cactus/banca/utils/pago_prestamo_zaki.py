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
    monto_total = request['total_amount']

    try:
        ordenante = User.objects.get(username=settings.USERNAME_ZAKI)
    except Exception as ex:
        db_logger.warning(
            f"[ZAKI crear_prestamo] Usuario Zaki no encontrado. ex: {ex}")
        return {
            'error': -24710
        }

    if float(abono) > ordenante.Uprofile.saldo_cuenta:
        db_logger.warning("[ZAKI crear_prestamo] Saldo Zaki insuficiente")
        return {
            'error': -24711
        }

    user_beneficiario = User.objects.filter(
        username=username,
        is_active=True)
    if user_beneficiario.count() == 0:
        db_logger.warning(
            f"[ZAKI crear_prestamo] User {username} no encontrado o inactivo.")
        return {
            'error': -24712
        }
    user_beneficiario = user_beneficiario.last()

    prestamos = user_beneficiario.prestamos_zaki.all()
    num_prestamos = prestamos.filter(status="P").count()
    if num_prestamos > 0:
        db_logger.warning(
            f"[ZAKI crear_prestamo] User {username} ya cuenta con préstamo.")
        return {
            'error': -24714
        }

    fecha = datetime.now()
    status = StatusTrans.objects.get(nombre="exito")
    tipo_enviada = TipoTransaccion.objects.get(codigo=200)  # Prestamo enviada
    tipo_recibida = TipoTransaccion.objects.get(
        codigo=201)  # Prestamo recibida
    claveR = randomString()
    monto2F = "{:.2f}".format(round(float(abono), 2))
    monto_total2F = "{:.2f}".format(round(float(monto_total), 2))

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
    prestamo = PrestamoZakiTransaccion.objects.create(
        user=user_beneficiario,
        fechaOperacion=fecha,
        enviada_prestamo=enviada_trans,
        recibida_prestamo=recibida_trans,
        monto=monto2F,
        monto_total=monto_total2F,
        status="P"
    )

    ordenante.Uprofile.saldo_cuenta -= round(float(abono), 2)
    ordenante.Uprofile.save()
    user_beneficiario.Uprofile.saldo_cuenta += round(float(abono), 2)
    user_beneficiario.Uprofile.save()

    msg = "[Zaki crear_prestamo] Exitoso para el usuario: {} por {}".format(
        username,
        abono)
    db_logger.info(msg)

    return {
        "created": True,
        "inguzId": prestamo.id
    }


def abonar_prestamo(request):
    # Permissions: Sólo permitida al usuario Zaki
    # {"username": "5529641640", "amount": 50}
    if 'username' not in request or 'amount' not in request:
        db_logger.warning(
            f"[ZAKI abonar_prestamo] Bad request, from zaki: {request}")

        return {
            'error': -24719
        }
    username = request['username']
    abono = request['amount']

    try:
        user_zaki = User.objects.get(username=settings.USERNAME_ZAKI)
    except Exception as ex:
        db_logger.warning(
            f"[ZAKI abonar_prestamo] Usuario Zaki no encontrado. ex: {ex}")
        return {
            'error': -24713
        }

    ordenante = User.objects.filter(
        username=username,
        is_active=True)
    if ordenante.count() == 0:
        db_logger.warning(
            f"[ZAKI abono_prestamo] User {username} no encontrado o inactivo.")
        return {
            'error': -24715
        }
    ordenante = ordenante.last()
    prestamos = ordenante.prestamos_zaki.all()
    num_prestamos = prestamos.filter(status="P").count()
    if num_prestamos == 0:
        db_logger.warning(
            f"[ZAKI abonar_prestamo] User {username} sin préstamo activo.")
        return {
            'error': -24716
        }

    if num_prestamos > 1:
        db_logger.warning(
            f"[ZAKI abonar_prestamo] User {username} con múltiples préstamos.")
        return {
            'error': -24717
        }

    prestamo = prestamos.get(status="P")

    if float(abono) > ordenante.Uprofile.saldo_cuenta:
        db_logger.warning(
            "[ZAKI abonar_prestamo] Saldo Usuario insuficiente")
        return {
            'error': -24718
        }

    balance_previo = sum(
        list(
            map(
                lambda _abono: float(_abono.monto), prestamo.abonos.all()
            )
        )
    )

    if (balance_previo + float(abono)) > float(prestamo.monto_total):
        abono = float(prestamo.monto_total) - float(balance_previo)

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
        concepto="Abono Zaki",
        claveRastreo=claveR
    )
    recibida_trans = Transaccion.objects.create(
        user=user_zaki,
        fechaValor=fecha,
        fechaAplicacion=fecha,
        monto=float(abono),
        statusTrans=status,
        tipoTrans=tipo_recibida,
        concepto="Abono Zaki",
        claveRastreo=claveR
    )
    pago = PagoZakiTransaccion.objects.create(
        prestamo=prestamo,
        user=ordenante,
        fechaOperacion=fecha,
        enviada_pago=enviada_trans,
        recibida_pago=recibida_trans,
        monto=monto2F
    )
    ordenante.Uprofile.saldo_cuenta -= round(float(abono), 2)
    ordenante.Uprofile.save()
    user_zaki.Uprofile.saldo_cuenta += round(float(abono), 2)
    user_zaki.Uprofile.save()

    msg = "[Zaki abonar_prestamo] abono para el usuario: {} por {}".format(
        username,
        abono)
    db_logger.info(msg)

    balance = sum(
        list(
            map(
                lambda abono: float(abono.monto), prestamo.abonos.all()
            )
        )
    )

    liquidado = False
    if balance == float(prestamo.monto_total):
        prestamo.status = "L"
        prestamo.save()
        liquidado = True
        msg = "[Zaki abonar_prestamo] Liquidado para user: {} por {}".format(
            username,
            abono)
        db_logger.info(msg)

    return {
        "created": True,
        "inguzId": pago.id,
        "liquidado": liquidado
    }
