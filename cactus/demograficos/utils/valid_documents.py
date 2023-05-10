from django.contrib.auth.models import User
from demograficos.models import DocAdjunto
from datetime import datetime
import logging
import ast


db_logger = logging.getLogger('db')


def validate_information(user, information):

    user_ = User.objects.get(username=user)

    nombre = user_.first_name
    apaterno = user_.last_name
    amaterno = user_.Uprofile.apMaterno
    curp = user_.Uprofile.curp
    fecha = user_.Uprofile.fecha_nacimiento
    fecha = fecha.strftime("%d/%m/%Y")
    _user_ = [apaterno, amaterno, curp, fecha]
    if isinstance(nombre, str) and len(nombre.split()) >= 2:
        for n in nombre.split():
            _user_.append(n)
    else:
        _user_.append(nombre)

    valid_information = [item.upper() for item in _user_]
    matched_strings = []

    for item in information:
        if item in valid_information:
            matched_strings.append(item)

    matched_count = len(matched_strings)
    total_count = len(valid_information)
    percentage = (matched_count / total_count) * 100
    if percentage >= 95:
        user_.Uprofile.ocr_ine_validado = True
        user_.Uprofile.save()
        return True, matched_strings
    else:
        msg = f"[Ine Validation] Ine no coincide con el usuario {user}"
        db_logger.warning(msg)
        raise Exception("Ine no coincide con el usuario: ", user)


def validate_information_ine_back(user, back_information):

    user_ = User.objects.get(username=user)
    front = DocAdjunto.objects.filter(user=user_, tipo='1').last()
    if front.validado is True:
        valid_front = ast.literal_eval(front.validacion_frontal)
        a = back_information[-1]
        b = back_information[-2]
        back_info = []
        matched_strings = []
        if isinstance(a, str) and len(a.split()) >= 2:
            for string in a.split():
                back_info.append(string)
        if isinstance(b, str) and len(b.split()) > 1:
            date = b.split()[0]
            date = date[0:6]
            date = datetime.strptime(date, '%y%m%d')
            date = datetime.strftime(date, '%d/%m/%Y')
            back_info.append(date)

        for item in back_info:
            if item in valid_front:
                matched_strings.append(item)

        matched_count = len(matched_strings)
        total_count = len(back_info)
        percentage = (matched_count / total_count) * 100
        if percentage >= 95:
            user_.Uprofile.ocr_ine_back_validado = True
            user_.Uprofile.save()
            return True
        else:
            msg = f"[Ine Back Validation] Ine no coincide con el usuario " \
                  f"{user}"
            db_logger.warning(msg)
            raise Exception("Ine no coincide con el usuario: ", user)
