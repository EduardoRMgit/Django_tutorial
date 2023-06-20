import logging
from django.contrib.auth.models import User


db_logger = logging.getLogger('db')


def comprobar_clabe_curp(request):
    curp_valido = False
    dicc = {}
    try:
        curp_ = request['curp']
        clabe = request['clabe']
        curp = User.objects.filter(
            is_active=True,
            Uprofile__CuentaClabe=clabe,
            Uprofile__curp=curp_)
        if curp:
            curp_valido = True
            msg_logg = "[Servicio Zaki CLABE-CURP] {}.".format(
                f"CURP {curp_} Valido")
            db_logger.info(msg_logg)
        elif curp >= 2:
            msg_logg = "[Error Servicio Zaki CLABE-CURP] {}.".format(
                f"Hay varios usuarios con el mismo curp {curp_}")
            db_logger.info(msg_logg)
        if not curp_valido:
            msg_logg = "[Servicio Zaki CLABE-CURP] {}.".format(
                f"CURP {curp_}  No valido")
            db_logger.error(msg_logg)

        dicc['curp_valido'] = curp_valido

    except Exception as ex:
        msg = f"[Servicio Zaki]:{ex}"
        db_logger.error(msg)
        dicc['error'] = "bad request"
    return dicc


def comprobar_username_curp(request):
    curp_valido = False
    dicc = {}
    try:
        curp_ = request['curp']
        username = request['username']
        curp = User.objects.filter(
            is_active=True,
            username=username,
            Uprofile__curp=curp_).count()
        if curp:
            curp_valido = True
            msg_logg = "[Servicio Zaki USERNAME-CURP] {}.".format(
                f"CURP {curp_} Valido")
            db_logger.info(msg_logg)
        elif curp >= 2:
            msg_logg = "[Error Servicio Zaki USERNAME-CURP] {}.".format(
                f"Hay varios usuarios con el mismo curp {curp_}")
            db_logger.info(msg_logg)
        if not curp_valido:
            msg_logg = "[Servicio Zaki USERNAME-CURP] {}.".format(
                f"CURP {curp_}  No valido")
            db_logger.error(msg_logg)

        dicc['curp_valido'] = curp_valido

    except Exception as ex:
        msg = f"[Servicio Zaki]:{ex}"
        db_logger.error(msg)
        dicc['error'] = "bad request"
    return dicc


def comprobar_username(request):

    msg = f"[Zaki comprobar_username()] Petición recibida: {request}"
    db_logger.info(msg)

    username = request.get('username', False)
    if not username:
        return {
            'error': 'bad_request'
        }
    user = User.objects.filter(username=username,
                               is_active=True)
    existe = True
    if user.count() == 0:
        existe = False

    res = {
        'existe_username': existe
    }

    msg = f"[Zaki comprobar_username()] Respuesta: {res}"
    db_logger.info(msg)

    return res


def comprobar_curp(request):
    curp_valido = False
    dicc = {}
    try:
        curp_ = request['curp']
        curp = User.objects.filter(
            is_active=True,
            Uprofile__curp=curp_).count()
        if curp == 1:
            curp_valido = True
            msg_logg = "[Servicio Zaki CURP] {}.".format(
                f"CURP {curp_} Valido")
            db_logger.info(msg_logg)
        elif curp >= 2:
            msg_logg = "[Error Servicio Zaki CURP] {}.".format(
                f"Hay varios usuarios con el mismo curp {curp_}")
            db_logger.info(msg_logg)
        if not curp_valido:
            msg_logg = "[Servicio Zaki CURP] {}.".format(
                f"CURP {curp_}  No valido")
            db_logger.error(msg_logg)

        dicc['curp_valido'] = curp_valido

    except Exception as ex:
        msg = f"[Servicio Zaki CURP]:{ex}"
        db_logger.error(msg)
        dicc['error'] = "bad request"
    return dicc
