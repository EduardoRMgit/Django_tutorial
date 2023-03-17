import logging
from django.contrib.auth.models import User

db_logger = logging.getLogger('db')


def comprobar_curp(request):
    curp_valido = False
    try:
        curp_ = request['curp']
        username = request['username']
        curp = User.objects.get(
            is_active=True,
            username=username,
            Uprofile__curp=curp_).count()
        if curp:
            curp_valido = True
            msg_logg = "[Servicio Zaki] {}.".format(
                f"CURP {curp_} Valido")
            db_logger.info(msg_logg)
        elif curp >= 2:
            msg_logg = "[Error Servicio Zaki] {}.".format(
                f"Hay varios usuarios con el mismo curp {curp_}")
            db_logger.info(msg_logg)
        if not curp_valido:
            msg_logg = "[Servicio Zaki] {}.".format(
                        f"CURP {curp}  No valido")
            db_logger.error(msg_logg)

        dicc = {}
        dicc['curp_valido'] = curp_valido
        return dicc

    except Exception as ex:
        msg = f"[Servicio Zaki]:{ex}"
        db_logger.error(msg)
