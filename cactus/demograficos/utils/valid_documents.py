from django.contrib.auth.models import User
import logging


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
    if isinstance(nombre, str) and len(nombre.split()) == 2:
        nombre1, nombre2 = nombre.split()
        _user_.append(nombre1)
        _user_.append(nombre2)
    elif isinstance(nombre, str) and len(nombre.split()) == 3:
        nombre1, nombre2, nombre3 = nombre.split()
        _user_.append(nombre1)
        if nombre2 == 'de':
            nombre2 = nombre2 + nombre3
            _user_.append(nombre2)
        else:
            _user_.append(nombre2)
            _user_.append(nombre3)
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
    if percentage >= 100:
        user_.Uprofile.ocr_ine_validado = True
        user_.Uprofile.save()
    else:
        msg = f"[Ine Validation] Ine no coincide con el usuario {user}"
        db_logger.warning(msg)
        raise Exception("Ine no coincide con el usuario: ", user)


def validate_information_ine_back(front_information, back_information):

    print("hello world")
