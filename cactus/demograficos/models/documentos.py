# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import User


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


class TipoComprobante(models.Model):

    tipo = models.CharField(max_length=15, blank=True, null=True)

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
    imagen = models.ImageField(max_length=2048,
                               blank=True,
                               null=True)
    imagen_url = models.URLField(
        max_length=2048,
        null=True,
        blank=True
    )
    ruta = models.CharField(max_length=50, blank=True, null=True)
    tipo = models.ForeignKey(
        DocAdjuntoTipo,
        related_name='tipo_documento',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    tipo_comprobante = models.ForeignKey(
        TipoComprobante,
        related_name='tipo_comprobante',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    validado = models.BooleanField(default=False, blank=True, null=True)
    validado_operador = models.BooleanField(
        default=False,
        blank=True,
        null=True)
    user = models.ForeignKey(
        User,
        related_name='user_documento',
        on_delete=models.CASCADE,
    )
    orden = models.BooleanField(default=True, help_text="1 es frente 0 \
        es reverso", blank=True, null=True)
    fechaCreado = models.DateTimeField(auto_now_add=True, blank=True,
                                       null=True)
    validacion_frontal = models.TextField(blank=True, null=True)
    motivo_rechazo = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{} de {}".format(self.tipo, self.user)


class MotivoRechazoDoc(models.Model):
    tipos_doc = (
        ("I", "INE"),
        ("C", "Comprobante")
    )
    motivo = models.CharField(max_length=1028, null=True)
    tipo = models.CharField(choices=tipos_doc,
                            max_length=16, null=True)
    codigo = models.CharField(max_length=4, null=True)

    def __str__(self):
        return f"{self.motivo}"


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
