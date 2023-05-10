from django.contrib.auth.models import User
from demograficos.models import Direccion
from demograficos.utils.meses import normalizeDates, meses
from datetime import datetime, timedelta
import re


def validate_cfe(user, list):

    months = {
        'ENE': '01',
        'FEB': '02',
        'MAR': '03',
        'ABR': '04',
        'MAY': '05',
        'JUN': '06',
        'JUL': '07',
        'AGO': '08',
        'SEP': '09',
        'OCT': '10',
        'NOV': '11',
        'DIC': '12'
    }

    date = None
    datescfe = []
    dates = []
    datesformated = []

    for i in range(len(list) - 2):
        if (
            list[i].isdigit()
            and len(list[i]) == 2
            and list[i + 1] in months
            and len(list[i + 2]) == 2
        ):
            day = list[i]
            month = months[list[i + 1]]
            year = list[i + 2]
            date = f"{day}/{month}/{year}"
            datescfe.append(date)
    for i in range(0, len(datescfe)):
        item = datescfe[i]
        a = item.replace('/', '-')
        dates.append(a)

    for i in range(0, len(dates)):
        try:
            item = dates[i]
            date = datetime.strptime(item.replace('/', '-'), "%d-%m-%y")
            datesformated.append(date)
        except Exception as e:
            raise Exception(e)

    try:
        hoy = datetime.now()
        if len(datesformated) > 1:
            a = datesformated[0]
            b = datesformated[1]
            if a > b:
                comparacion = (hoy - a > timedelta(days=90))
                if comparacion:
                    raise Exception("Comprobante invalido mayor a 3 meses")
                else:
                    pass
            elif b > a:
                comparacion = (hoy - b > timedelta(days=90))
                if comparacion:
                    raise Exception("Comprobante invalido mayor a 3 meses")
                else:
                    pass
        else:
            a = datesformated[0]
            comparacion = (hoy - a > timedelta(days=90))
            if comparacion:
                raise Exception("Comprobante invalido mayor a 3 meses")
            else:
                pass
    except Exception as ex:
        raise Exception(ex)

    matched_strings = []
    user = User.objects.get(username=user)
    user_direccion = Direccion.objects.filter(user=user).last()
    calle = user_direccion.calle
    no_exterior = user_direccion.num_ext
    codigopostal = user_direccion.codPostal
    colonia = user_direccion.colonia
    municipio = user_direccion.delegMunicipio
    estado = user_direccion.estado
    direccion = [no_exterior, codigopostal]
    no_interior = user_direccion.num_int
    if no_interior is not None:
        direccion.append(no_interior)
    if isinstance(calle, str) and len(calle.split()) >= 2:
        for n in calle.split():
            direccion.append(n)
    else:
        direccion.append(calle)
    if isinstance(colonia, str) and len(colonia.split()) >= 2:
        for n in colonia.split():
            direccion.append(n)
    else:
        direccion.append(colonia)
    if isinstance(municipio, str) and len(municipio.split()) >= 2:
        for n in municipio.split():
            direccion.append(n)
    else:
        direccion.append(municipio)
    if isinstance(estado, str) and len(estado.split()) >= 2:
        for n in municipio.split():
            direccion.append(n)
    else:
        direccion.append(municipio)
    direccion = [item.upper() for item in direccion]
    list = [item.upper() for item in list]

    for item in direccion:
        if item in list:
            matched_strings.append(item)

    matched_count = len(matched_strings)
    total_count = len(direccion)
    percentage = (matched_count / total_count) * 100

    if percentage >= 80:
        user.Uprofile.ocr_comprobante_validado = True
        user.Uprofile.save()
        return True


def validate_telmex(user, list):

    reg = r"(0[1-9]|[12][0-9]|3[01])([\/|.|\-|\s])([A-Za-z0-9])+" \
          r"([\/|.|\-|\s])([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])"

    date_pattern = f'{reg}$'
    pattern = re.compile(date_pattern)
    string = "C.P."
    found = False
    sufix = "-CR"

    user = User.objects.get(username=user)
    user_direccion = Direccion.objects.filter(user=user).last()
    calle = user_direccion.calle
    no_exterior = user_direccion.num_ext
    codigopostal = user_direccion.codPostal
    colonia = user_direccion.colonia
    municipio = user_direccion.delegMunicipio
    estado = user_direccion.estado
    direccion = [no_exterior, codigopostal]
    no_interior = user_direccion.num_int
    if no_interior is not None:
        direccion.append(no_interior)
    if isinstance(calle, str) and len(calle.split()) >= 2:
        for n in calle.split():
            direccion.append(n)
    else:
        direccion.append(calle)
    if isinstance(colonia, str) and len(colonia.split()) >= 2:
        for n in colonia.split():
            direccion.append(n)
    else:
        direccion.append(colonia)
    if isinstance(municipio, str) and len(municipio.split()) >= 2:
        for n in municipio.split():
            direccion.append(n)
    else:
        direccion.append(municipio)
    if isinstance(estado, str) and len(estado.split()) >= 2:
        for n in municipio.split():
            direccion.append(n)
    else:
        direccion.append(municipio)
    direccion = [item.upper() for item in direccion]
    list = [item.upper() for item in list]
    direccion = [item.upper() for item in direccion]
    direccion_extraida = []
    valid = []
    fechas = []
    matched_strings = []
    for item in list:
        if found:
            if item.endswith(sufix):
                cp = item.split("-")[0]
                valid.append(cp)
            found = False
        if string in item:
            found = True
        if re.match(pattern, item):
            date = re.match(pattern, item)
            fechas.append(date.group())
        if item in direccion:
            direccion_extraida.append(item)
    for item in direccion:
        if item in direccion_extraida:
            matched_strings.append(item)

    fechas = normalizeDates(fechas)

    datest = []

    for item in fechas:
        if len(item) > 8:
            datest.append(datetime.strptime(item, "%d-%m-%Y"))

    if len(datest) >= 2:
        try:
            a = datest[0]
            b = datest[1]
        except Exception as ex:
            raise Exception("Error al asignar fechas", ex)
        try:
            if b > a:
                hoy = datetime.now()
                comparacion = (hoy - a > timedelta(days=90))
                if comparacion:
                    raise Exception("Comprobante invalido mayor a 3 meses")
                else:
                    pass
            elif a > b:
                hoy = datetime.now()
                comparacion = (hoy - b > timedelta(days=90))
                if comparacion:
                    raise Exception("Comprobante invalido mayor a 3 meses")
                else:
                    pass
        except Exception as ex:
            raise Exception("Error al validar vigencia del comprobante", ex)

    matched_count = len(matched_strings)
    total_count = len(direccion)
    percentage = (matched_count / total_count) * 100
    if percentage >= 80:
        user.Uprofile.ocr_comprobante_validado = True
        user.Uprofile.save()
        return True


def validate_izzi(user, list):

    reg = r"(0[1-9]|[12][0-9]|3[01])([\/|.|\-|\s])([A-Za-z0-9])+" \
          r"([\/|.|\-|\s])([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])"

    date_pattern = f'{reg}$'
    pattern = re.compile(date_pattern)
    date = []
    datesizzi = []
    datesizziformated = []

    for item in list:
        if re.match(pattern, item):
            dates = re.match(pattern, item)
            date.append(dates.group())

    for item in date:
        dates = meses(item)
        datesizzi.append(dates)
    for i in range(0, len(datesizzi)):
        try:
            item = datesizzi[i]
            dates = datetime.strptime(item, "%d-%m-%y")
            datesizziformated.append(dates)
        except Exception as e:
            raise Exception(e)

    a = datesizziformated[0]
    b = datesizziformated[1]
    hoy = datetime.now()
    if a > b:
        comparacion = (hoy - a > timedelta(days=90))
        if comparacion:
            raise Exception("Comprobante invalido mayor a 3 meses")
        else:
            pass
    elif b > a:
        comparacion = (hoy - b > timedelta(days=90))
        if comparacion:
            raise Exception("Comprobante invalido mayor a 3 meses")
        else:
            pass

    matched_strings = []
    user = User.objects.get(username=user)
    user_direccion = Direccion.objects.filter(user=user).last()
    calle = user_direccion.calle
    no_exterior = user_direccion.num_ext
    codigopostal = user_direccion.codPostal
    colonia = user_direccion.colonia
    municipio = user_direccion.delegMunicipio
    estado = user_direccion.estado
    direccion = [no_exterior, codigopostal]
    no_interior = user_direccion.num_int
    if no_interior is not None:
        direccion.append(no_interior)
    if isinstance(calle, str) and len(calle.split()) >= 2:
        for n in calle.split():
            direccion.append(n)
    else:
        direccion.append(calle)
    if isinstance(colonia, str) and len(colonia.split()) >= 2:
        for n in colonia.split():
            direccion.append(n)
    else:
        direccion.append(colonia)
    if isinstance(municipio, str) and len(municipio.split()) >= 2:
        for n in municipio.split():
            direccion.append(n)
    else:
        direccion.append(municipio)
    if isinstance(estado, str) and len(estado.split()) >= 2:
        for n in municipio.split():
            direccion.append(n)
    else:
        direccion.append(municipio)
    direccion = [item.upper() for item in direccion]
    list = [item.upper() for item in list]

    for item in direccion:
        if item in list:
            matched_strings.append(item)

    matched_count = len(matched_strings)
    total_count = len(direccion)
    percentage = (matched_count / total_count) * 100

    if percentage >= 80:
        user.Uprofile.ocr_comprobante_validado = True
        user.Uprofile.save()
        return True


def validate_total(user, list):

    reg = r"(0[1-9]|[12][0-9]|3[01])([\/)([A-Za-z0-9])+" \
          r"([\/])([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])"

    date_pattern = f'{reg}$'
    pattern = re.compile(date_pattern)

    date = []
    datestotal = []

    for item in list:
        if re.match(pattern, item):
            dates = re.match(pattern, item)
            date.append(dates.group())

    for item in date:
        dates = item.replace('/', '-')
        dates = datetime.strptime(dates, "%d-%m-%Y")
        datestotal.append(dates)

    hoy = datetime.now()

    if len(datestotal) == 1:
        a = datestotal[0]
        comparacion = (hoy - a > timedelta(days=90))
        if comparacion:
            raise Exception("Comprobante invalido mayor a 3 meses")
        else:
            pass

    list = [item.upper() for item in list]
    matched_set = set()
    matched_strings = []

    user = User.objects.get(username=user)
    user_direccion = Direccion.objects.filter(user=user).last()
    calle = user_direccion.calle
    no_exterior = user_direccion.num_ext
    codigopostal = user_direccion.codPostal
    colonia = user_direccion.colonia
    municipio = user_direccion.delegMunicipio
    estado = user_direccion.estado
    direccion = [no_exterior, codigopostal]
    no_interior = user_direccion.num_int
    if no_interior is not None:
        direccion.append(no_interior)
    if isinstance(calle, str) and len(calle.split()) >= 2:
        for n in calle.split():
            direccion.append(n)
    else:
        direccion.append(calle)
    if isinstance(colonia, str) and len(colonia.split()) >= 2:
        for n in colonia.split():
            direccion.append(n)
    else:
        direccion.append(colonia)
    if isinstance(municipio, str) and len(municipio.split()) >= 2:
        for n in municipio.split():
            direccion.append(n)
    else:
        direccion.append(municipio)
    if isinstance(estado, str) and len(estado.split()) >= 2:
        for n in municipio.split():
            direccion.append(n)
    else:
        direccion.append(municipio)
    direccion = [item.upper() for item in direccion]

    for item in direccion:
        if item in list and item not in matched_set:
            matched_strings.append(item)
            matched_set.add(item)

    matched_count = len(matched_strings)
    total_count = len(direccion)
    percentage = (matched_count / total_count) * 100

    if percentage >= 80:
        user.Uprofile.ocr_comprobante_validado = True
        user.Uprofile.save()
        return True
