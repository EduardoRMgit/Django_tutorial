from django.contrib.auth.models import User
from demograficos.models import DocAdjunto
from datetime import datetime
import logging
import ast
import re


db_logger = logging.getLogger('db')


def validate_information(user, information):

    user_ = User.objects.get(username=user)

    vigencia = False
    try:
        keyword = 'VIGENCIA'
        años = []

        for item in range(len(information) - 1):
            if information[item] == keyword:
                year = re.search(r"\d{4}", information[item + 1])
                if year:
                    años.append(year.group())

        for i in años:
            try:
                valida = int(i)
                año_actual = datetime.now().year
                año_valido = datetime(valida, 1, 1)
                if año_actual < año_valido.year:
                    vigencia = True
                elif año_actual > año_valido.year:
                    return False, ("Ine no vigente")
            except Exception as ex:
                raise Exception(ex)

    except Exception:
        año_actual = datetime.now().year
        pattern = r"\d{4}-d{4}"
        años = []

        for item in information:
            match = re.search(pattern, item)
            if match:
                años.append(match.group())

        año = años[0].split('-')
        if len(año) == 2:
            try:
                a = año[0]
                b = año[1]
                if a < b:
                    b = datetime(b, 1, 1)
                    if año_actual < b.year:
                        vigencia = True
                    elif año_actual > b.year:
                        return False, ("Ine no vigente")
            except Exception as ex:
                raise Exception(ex)

    if vigencia is True:

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
            return False, ("Documento en proceso de validacion")


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
            return True, ("ok")
        else:
            msg = f"[Ine Back Validation] Ine no coincide con el usuario " \
                  f"{user}"
            db_logger.warning(msg)
            return False, ("Documento en proceso de validacion")
    else:
        return False, ("Error al validar")
