import cv2
from PIL import Image
from pytesseract import Output
import pytesseract
import io
import re
import logging
import requests
import numpy as np


db_logger = logging.getLogger('db')


def change_string(string):
    character = (
        ("O", "0"),
        ("D", "0"),
        ("S", "5"),
        ("I", "1"),
    )
    for a, b in character:
        string = string.replace(a, b).replace(a, b)
    return string


def preprocessing(img):
    dims = (1200, 1200)
    if img.shape[0] > 1000 and img.shape[1] > 1600:
        img = cv2.resize(img, dims, interpolation=cv2.INTER_AREA)
    if img.shape[0] < 1000 and img.shape[1] <= 1600:
        img = cv2.resize(img, dims, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    adaptive = cv2.adaptiveThreshold(blur,
                                     255,
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY,
                                     9, 3)
    return (img, gray, blur, adaptive)


def img_scratch(img):
    config_tesseract = '--tessdata-dir tessdata'
    result = pytesseract.image_to_data(img,
                                       config=config_tesseract,
                                       lang='spa',
                                       output_type=Output.DICT)
    print(result)
    list = []

    min_confidence = 0
    curp_regex = ('^[A-Z]{4}[0-9]{6}[H,M][A-Z]{5}[0-9A-Z]{2}')
    try:
        pattern = re.compile(curp_regex)
        for i in range(0, len(result['text'])):
            confidence = result['conf'][i]
            if confidence > min_confidence:
                text = result['text'][i]
                list.append(text)
                if re.match(pattern, text):
                    a = re.match(pattern, text)
                    a = a.group()
        return a
    except Exception as ex:
        msg = f"[Ine Validation] Error al procesar imagen: {ex}"
        db_logger.warning(msg)


def curp_validated(url, user):

    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    curp = img_scratch(img)
    if not curp:
        pix = np.array(img)
        a, b, c, d = preprocessing(pix)
        curp = img_scratch(b)
        if not curp:
            curp = img_scratch(c)
            if not curp:
                curp = img_scratch(d)
                if not curp:
                    raise Exception("Imagen Invalida")

    x = curp[-2:]
    if not x.isnumeric():
        y = change_string(x)
        curp = curp.replace(curp[-2:], y)
    if curp == user.Uprofile.curp:
        user.Uprofile.ocr_ine_validado = True
        user.save()
        return ("Ine valida, CURP correcto")
