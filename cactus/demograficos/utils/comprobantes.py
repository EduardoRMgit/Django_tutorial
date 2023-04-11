from demograficos.utils.meses import meses
from demograficos.utils.dates import normalizeDates
import pytesseract
from PIL import Image
from pytesseract import Output
import io
import datetime
import requests
import re
import logging


db_logger = logging.getLogger('db')


def validacionComprobantes(tipo, url, user):

    try:
        reg = r"(0[1-9]|[12][0-9]|3[01])([\/|.|\-|\s])([A-Za-z0-9])+" \
              r"([\/|.|\-|\s])([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])"

        response = requests.get(url)
        img = Image.open(io.BytesIO(response.content))
        img = img.convert('RGB')
        config_tesseract = '--tessdata-dir tessdata'
        result = pytesseract.image_to_data(img,
                                           config=config_tesseract,
                                           lang='por',
                                           output_type=Output.DICT)
        list = []
        list.append(result)
        min_confidence = 0
        dates = []
        listf = []
        date_pattern = f'{reg}$'
        pattern = re.compile(date_pattern)
        for i in range(0, len(result['text'])):
            confidence = result['conf'][i]
            if confidence > min_confidence:
                text = result['text'][i]
                if re.match(pattern, text):
                    listf.append(text)
                    a = re.match(pattern, text)
                    a = a.group()
                    dates.append(a)

        print(dates)
    except Exception as ex:
        msg = f"[Validacion Comprobantes] Error al procesar imagen: {ex}"
        db_logger.warning(msg)
    try:
        if tipo == '1':
            return ("Comprobante CFE validar con servicio al cliente")
        elif tipo == '2':
            dates = normalizeDates(dates)
            datesn = []
            for date in dates:
                try:
                    if len(date) > 8:
                        x = datetime.datetime.strptime(
                            date, "%d-%m-%Y")
                        datesn.append(x)
                except Exception as ex:
                    msg = f"[Comprobante Telmex] Error al validar el " \
                          f"comprobante {ex}"
                    db_logger.warning(msg)
            try:
                a = datesn[0]
                b = datesn[1]
            except Exception as ex:
                msg = f"[Comprobante Telmex] Error, lista datesn  no " \
                      f"contiene 2 fechas {ex}"
                db_logger.warning(msg)
            try:
                if b > a:
                    hoy = datetime.datetime.now()
                    comparacion = (hoy - a > datetime.timedelta(days=90))
                    if comparacion:
                        return ("Comprobante mayor a 3 meses")
                    else:
                        user.Uprofile.ocr_comprobante_validado = True
                        user.save()
                        return ("Comprobante Valido")
                elif a > b:
                    hoy = datetime.datetime.now()
                    comparacion = (hoy - b > datetime.timedelta(days=90))
                    if comparacion:
                        return ("Comprobante mayor a 3 meses")
                    else:
                        user.Uprofile.ocr_comprobante_validado = True
                        user.save()
                        return ("Comprobante Valido")
            except Exception as ex:
                msg = f"[Validacion Telmex] Error no fue posible validar " \
                      f"el compronte {ex}"
                db_logger.warning(msg)
        elif tipo == '3':
            datesn = []
            datesh = []
            for date in dates:
                try:
                    x = meses(date)
                    datesn.append(x)
                except Exception as ex:
                    msg = f"[Comprobante Izzi] Error, no se logro convertir " \
                          f"mes a formato numerico {ex}"
                    db_logger.warning(msg)
            for date in datesn:
                try:
                    newdate = datetime.datetime.strptime(date, "%d-%m-%y")
                    datesh.append(newdate)
                except Exception as ex:
                    msg = f"[Comprobante Izzi] Error, no se logro dar " \
                          f"el formato necesario a las fechas {ex}"
                    db_logger.warning(msg)
            try:
                a = datesh[0]
                b = datesh[1]
            except Exception as ex:
                msg = f"[Comprobante Izzi] Error, lista dates  no " \
                      f"contiene 2 fechas para comparar {ex}"
                db_logger.warning(msg)
            hoy = datetime.datetime.now()
            if a > b:
                comparacion = (hoy - a > datetime.timedelta(
                    days=90))
                if comparacion:
                    return ("Comprobante mayor a 3 meses")
                else:
                    user.Uprofile.ocr_comprobante_validado = True
                    user.save()
                    return ("Comprobante Valido")
            elif b > a:
                comparacion = (hoy - b > datetime.timedelta(
                    days=90))
                if comparacion:
                    return ("Comprobante mayor a 3 meses")
                else:
                    user.Uprofile.ocr_comprobante_validado = True
                    user.save()
                    return ("Comprobante Valido")
        elif tipo == '4':
            datesn = []
            datesh = []
            for date in dates:
                try:
                    x = meses(date)
                    datesn.append(x)
                except Exception as ex:
                    msg = f"[Comprobante TotalPlay] Error, no se logró " \
                          f"convertir el mes a formato numerico {ex}"
                    db_logger.warning(msg)
            for date in datesn:
                try:
                    newdate = datetime.datetime.strptime(date, "%d/%m/%Y")
                    datesh.append(newdate)
                except Exception as ex:
                    msg = f"[Comprobante TotalPlay] Error, no se logro dar " \
                          f"el formato necesario a las fechas {ex}"
                    db_logger.warning(msg)
            hoy = datetime.datetime.now()
            if len(datesh) >= 2:
                try:
                    a = datesh[0]
                    b = datesh[1]
                except Exception as ex:
                    msg = f"[Comprobante TotalPlay] Lista solo contiene 1 " \
                          f"indice {ex}"
                    db_logger.warning(msg)
            else:
                a = datesh[0]
                comparacion = (hoy - a > datetime.timedelta(
                    days=90))
                if comparacion:
                    return ("Comprobante mayor a 3 meses")
                else:
                    user.Uprofile.ocr_comprobante_validado = True
                    user.save()
                    return ("Comprobante Valido")

    except Exception as ex:
        msg = f"[Validacion Comprobante] Error, al validar comprobante {ex} "
        db_logger.warning(msg)
