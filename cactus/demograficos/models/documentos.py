# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import pytesseract
from PIL import Image
from pytesseract import Output
import io
import requests


# Catalogo de documentos adjuntos
class DocAdjuntoTipo(models.Model):
    """Document type uploaded by the user.

    ``Attributes:``

        - tipo (char): can be INE(1),
         INE REVERSO (2), COMPROBANTE DE DOMICILIO (3), etc.

    """
    tipo = models.CharField(max_length=30)

    def __str__(self):
        return self.tipo


class DocAdjunto(models.Model):
    """Document type uploaded by the user.

    ``Attributes:``

        - images (image): image taken for OCR.

        - ruta (char): url returned by the storage service provider.

        - tipo (foreign): many to one to the DocAdjuntoTipo model.

        - validado (boolean): if it's been approved by the OCR system or the \
            authorities.

        - orden (boolean): 1 equals the front of the document, 0 equals the \
            reverse face of the document.

        - fechaCreado (datetime): 1 equals the front of the document, 0 \
            equals the reverse face of the document.

    """

    # La ruta es dinamica, se construye con la "ruta"
    imagen = models.ImageField(upload_to='demograficos/docs', blank=True,
                               null=True)
    ruta = models.CharField(max_length=50, blank=True, null=True)
    tipo = models.ForeignKey(
        DocAdjuntoTipo,
        related_name='tipo_documento',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    validado = models.BooleanField(default=False, blank=True, null=True)
    user = models.ForeignKey(
        User,
        related_name='user_documento',
        on_delete=models.CASCADE,
    )
    orden = models.BooleanField(default=True, help_text="1 es frente 0 \
        es reverso", blank=True, null=True)
    fechaCreado = models.DateTimeField(auto_now_add=True, blank=True,
                                       null=True)

    def __str__(self):
        return "{} de {}".format(self.tipo, self.user)


# Guarda la imagen subida a algun usuario para verla directo desde user profile
@receiver(post_save, sender=DocAdjunto)
def imagen(sender, instance, created, **kwargs):
    if created:
        user_ = User.objects.get(id=instance.user_id)
        uprofile = user_.Uprofile
        # curp = uprofile.curp
        if instance.tipo_id == 1:
            uprofile.ineCaptura = instance.imagen
            url = "{}{}".format(
                'http://127.0.0.1:8000/media/', instance.imagen)
            response = requests.get(url)
            img = Image.open(io.BytesIO(response.content))
            config_tesseract = '--tessdata-dir tessdata'
            result = pytesseract.image_to_data(img,
                                               config=config_tesseract,
                                               lang='spa',
                                               output_type=Output.DICT)
            list = []
            list.append(result)
            print(list)
            min_confidence = 40
            listf = []
            for i in range(0, len(result['text'])):
                confidence = result['conf'][i]
                if confidence > min_confidence:
                    text = []
                    text = result['text'][i]
                    # print(text)
                    # dicc['key'] = text
                    listf.append(text)
            # print(listf)
            # print(curp)
            # for x in listf:
            #     if (x == ''):
            #         print("Curp valido")
        elif instance.tipo_id == 2:
            uprofile.ineReversoCaptura = instance.imagen
            url = "{}{}".format(
                'http://127.0.0.1:8000/media/', instance.imagen)
            response = requests.get(url)
            img = Image.open(io.BytesIO(response.content))
            config_tesseract = '--tessdata-dir tessdata'
            result = pytesseract.image_to_data(img,
                                               config=config_tesseract,
                                               output_type=Output.DICT)
            print(result)
            list = []
            list.append(result)
            print(list)
            min_confidence = 15
            for i in range(0, len(result['text'])):
                confidence = result['conf'][i]
                if confidence > min_confidence:
                    text = result['text'][i]
                    dict = {}
                    dict = text
                    print(text)
                    print(dict)
        elif instance.tipo_id == 3:
            uprofile.comprobanteDomCaptura = instance.imagen
            # url = "{}{}".format(
            #     'http://127.0.0.1:8000/media/', instance.imagen)
            # response = requests.get(url)
            # img = Image.open(io.BytesIO(response.content))
            # config_tesseract = '--tessdata-dir tessdata'
            # result = pytesseract.image_to_data(img,
            #                                    config=config_tesseract,
            #                                    output_type=Output.DICT)
            # print(result)
            # list = []
            # list.append(result)
            # print(list)
            # min_confidence = 80
            # for i in range(0, len(result['text'])):
            #     confidence = result['conf'][i]
            #     if confidence > min_confidence:
            #         text = result['text'][i]
            #         print(text)
        uprofile.save()


class DocExtraction(models.Model):
    """guardar en esta tabla el dict extraido de la foto y la validacio"""
    documento = models.OneToOneField(DocAdjunto, on_delete=models.CASCADE,
                                     null=True)
    validacion = models.FloatField(null=True)
    diccionario = models.CharField(max_length=5000, null=True)
    detalles = models.CharField(max_length=5000, null=True)
    errores = models.CharField(max_length=5000, null=True)

    def __str__(self):
        return "{} de {}".format(self.documento.tipo, self.documento.user)


def get_info_dict(user):
    profile = user.Uprofile
    direccion = user.user_direccion.last()
    if user.first_name == '':
        name = user.username
    else:
        name = user.first_name
    info_dict = {
        "FIRST_NAME": name,
        "CALLE": direccion.calle,
        "COLONIA": (str(direccion.colonia) + ' ' + str(direccion.codPostal)),
        "ESTADO": direccion.entidadFed.clave,
        "DELEGACION_MUNICIPIO": '{}, {}'.format(direccion.delegMunicipio,
                                                direccion.ciudad),
        "NUMERO_EXT": direccion.num_ext,
        "NUMERO_INT": direccion.num_int,
        "NUMERO_INE": profile.numero_INE,
        "CURP": profile.curp,
        "SEXO": profile.sexo}

    return info_dict


def send_doc_ocr(user, doc):
    import requests
    import json
    import os

    site = os.getenv('SITE', 'local')

    base_url = 'http://localhost:8080'

    if site != 'local':
        base_url = 'http://138.68.39.247'

    url = base_url + '/OCRApp/api-token-auth/'

    # Ask for username and password
    input_name = 'inguz'
    input_pwd = ''

    payload = {'username': input_name, 'password': input_pwd}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    # Turn into a string
    rstring = r.content.decode('utf-8')
    token = json.loads(rstring)['token']

    if site != 'local':
        image_url = doc.imagen.url
    else:
        image_url = 'http://localhost:8000' + doc.imagen.url

    tipo_archivo = doc.tipo
    dict_info = json.dumps(get_info_dict(user))
    response = requests.get(image_url)
    f = response.content
    files = {'file': f}
    url = base_url + '/OCRApp/imagetest/'
    data = {'username': user.username,
            'tipo_archivo': tipo_archivo,
            'dict_info': dict_info}
    headers = {'Accept': 'application/json', 'Authorization':
               'Token {}'.format(token)}

    r = requests.post(url, files=files, data=data, headers=headers)
    rstring = r.content.decode('utf-8')
    # print('file {} sent to OCR'.format(doc.tipo))


def sendOCR(user):
    # print('try sending docs')
    tipo = DocAdjuntoTipo.objects.get(tipo="INE")
    doc = DocAdjunto.objects.filter(user=user,
                                    tipo=tipo).last()
    # print(DocAdjunto.objects.filter(user=user))
    # for doc in documentos:
    try:
        send_doc_ocr(user, doc)
    except Exception as e:
        print(e)
        pass
