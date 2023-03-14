import logging
from django.contrib.auth.models import User

db_logger = logging.getLogger('db')


def ZakiComprobar(request):
    curp_valido = False
    user_valido = False
    try:
        curp = request['curp']
        username = request['username']
        valida_curp = request['valida_curp']
        users = User.objects.all()
        for user in users:
            if valida_curp:
                if curp == user.Uprofile.curp:
                    curp_valido = True
                    msg_logg = "[Servicio Zaki] {}.".format(
                        f"CURP {curp} Valido")
                    db_logger.info(msg_logg)
            if username == user.username:
                user_valido = True
                msg_logg = "[Servicio Zaki] {}.".format(
                    f"Username {username} Valido")
                db_logger.info(msg_logg)
        if not user_valido:
            msg_logg = "[Servicio Zaki] {}.".format(
                        f"Username {username} No valido")
            db_logger.error(msg_logg)
        if not curp_valido:
            msg_logg = "[Servicio Zaki] {}.".format(
                        f"CURP {curp}  No valido")
            db_logger.error(msg_logg)

        dicc = {}
        dicc['username_valido'] = user_valido
        dicc['curp_valido'] = curp_valido
        return dicc

    except Exception as ex:
        msg = f"[Servicio Zaki]:{ex}"
        db_logger.error(msg)
