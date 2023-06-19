from demograficos.serializers import ImageDocSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from demograficos.models import (DocAdjunto,
                                 DocAdjuntoTipo,
                                 TipoComprobante)
from demograficos.utils.textract import (textract_ine,
                                         textract_ine_reverso,
                                         extract_comprobantes)
from demograficos.utils.valid_documents import (validate_information,
                                                validate_information_ine_back)
from demograficos.utils.comprobantes import (validate_cfe,
                                             validate_telmex,
                                             validate_izzi,
                                             validate_total)
from PIL import Image
from io import BytesIO

import boto3
from django.conf import settings
import os
from datetime import datetime
import logging


db_logger = logging.getLogger('db')


def get_file_url(archivo, file_path):
    from cactus.settings import (AWS_ACCESS_KEY_ID,
                                 AWS_SECRET_ACCESS_KEY,
                                 AWS_S3_REGION_NAME)

    client = boto3.client(
        's3',
        config=boto3.session.Config(signature_version='s3v4'),
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_S3_REGION_NAME)
    client.upload_fileobj(archivo,
                          settings.AWS_STORAGE_BUCKET_NAME,
                          file_path)
    file_url = client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': file_path,
            'ResponseContentType': 'image/jpeg'
        },
        ExpiresIn=1440,
        HttpMethod=None)
    return file_url


def upload_s3_docs(tipocomprobante, archivo, user):

    if tipocomprobante == '1':
        fecha = datetime.now().strftime("%d-%m-%Y_%H:%m:%s")
        nombre_archivo = f"comprobante_cfe_{user}_{fecha}.jpg"
        # directory = 'cfe'
        # file_path = os.path.join(
        #     directory,
        #     nombre_archivo
        # )
        # file_path = os.path.join('docs', file_path)
        file_path = os.path.join('docs/', nombre_archivo)
        file_url = get_file_url(archivo, file_path)
    elif tipocomprobante == '2':
        fecha = datetime.now().strftime("%d-%m-%Y_%H:%m:%s")
        nombre_archivo = f"comprobante_telmex_{user}_{fecha}.jpg"
        # directory = 'telmex'
        # file_path = os.path.join(
        #     directory,
        #     nombre_archivo
        # )
        # file_path = os.path.join('docs', file_path)
        file_path = os.path.join('docs/', nombre_archivo)
        file_url = get_file_url(archivo, file_path)
    elif tipocomprobante == '3':
        fecha = datetime.now().strftime("%d-%m-%Y_%H:%m:%s")
        nombre_archivo = f"comprobante_izzi_{user}_{fecha}.jpg"
        # directory = 'izzi'
        # file_path = os.path.join(
        #     directory,
        #     nombre_archivo
        # )
        # file_path = os.path.join('docs', file_path)
        file_path = os.path.join('docs/', nombre_archivo)
        file_url = get_file_url(archivo, file_path)
    elif tipocomprobante == '4':
        fecha = datetime.now().strftime("%d-%m-%Y_%H:%m:%s")
        nombre_archivo = f"comprobante_totalplay_{user}_{fecha}"
        # directory = 'totalplay'
        # file_path = os.path.join(
        #     directory,
        #     nombre_archivo
        # )
        # file_path = os.path.join('docs', file_path)
        file_path = os.path.join('docs/', nombre_archivo)
        file_url = get_file_url(archivo, file_path)
    return file_url, nombre_archivo, file_path


def upload_s3ine(archivo, user, tipo):

    if tipo == "1":
        fecha = datetime.now().strftime("%d-%m-%Y_%H:%m:%s")
        nombre_archivo = f"ine_frontal_{user}_{fecha}.jpg"
        # directory = 'ine'
        # file_path = os.path.join(
        #     directory,
        #     nombre_archivo
        # )
        # file_path = os.path.join('docs/', file_path)
        file_path = os.path.join('docs/', nombre_archivo)
        file_url = get_file_url(archivo, file_path)
    elif tipo == "2":
        fecha = datetime.now().strftime("%d-%m-%Y_%H:%m:%s")
        nombre_archivo = f"ine_reverso_{user}_{fecha}.jpg"
        # directory = 'ineReverso'
        # file_path = os.path.join(
        #     directory,
        #     nombre_archivo
        # )
        # file_path = os.path.join('docs/', file_path)
        file_path = os.path.join('docs/', nombre_archivo)
        file_url = get_file_url(archivo, file_path)
    return file_url, nombre_archivo, file_path


class ImageDoc(generics.CreateAPIView):
    serializer_class = ImageDocSerializer

    def post(self, request):
        imagen = request.data['imagen']
        tipo = request.data['tipo']
        user = request.data['user']
        user_ = User.objects.get(id=user)
        username = user_.username
        doctipo = DocAdjuntoTipo.objects.get(id=tipo)
        url = ""
        id = 0
        image = request.FILES['imagen']
        img = Image.open(image, mode='r')

        max_size = (1920, 1080)
        img.thumbnail(max_size, Image.ANTIALIAS)

        compressed_image = BytesIO()

        img.save(compressed_image, format='PNG')
        compressed_image.seek(0)
        imagen = compressed_image

        try:
            if request.data['tipo_comprobante'] != '':
                tipo_comprobante = request.data['tipo_comprobante']
                tipocomprobante = TipoComprobante.objects.get(
                    id=tipo_comprobante)
                if settings.USE_S3:
                    url, nombre_archivo, path = upload_s3_docs(
                        str(tipo_comprobante), imagen, username)
                    valida, informacion = extract_comprobantes(path)
                    if str(tipo_comprobante) == '1':
                        validacion, msg = validate_cfe(username, informacion)
                    if str(tipo_comprobante) == '2':
                        validacion, msg = validate_telmex(username,
                            informacion)
                    if str(tipo_comprobante) == '3':
                        validacion, msg = validate_izzi(username, informacion)
                    if str(tipo_comprobante) == '4':
                        validacion, msg = validate_total(username, informacion)
                    if validacion is True:
                        a = DocAdjunto.objects.create(
                            user=user_,
                            tipo=doctipo,
                            tipo_comprobante=tipocomprobante,
                            imagen=nombre_archivo,
                            imagen_url=url,
                            ruta=path,
                            validado=True)
                    elif validacion is False:
                        fotos = DocAdjunto.objects.filter(
                            user=user_, tipo=doctipo)
                        if len(fotos) < 3:
                            a = DocAdjunto.objects.create(
                                user=user_,
                                tipo=doctipo,
                                tipo_comprobante=tipocomprobante,
                                imagen=nombre_archivo,
                                imagen_url=url,
                                ruta=path)
                            return Response(
                                {
                                    'Mensaje': "Error al validar documento "
                                               "volver a tomar foto"
                                },
                                status=status.HTTP_200_OK)
                        elif len(fotos) >= 3:
                            return Response(
                                {
                                    'Mensaje': msg
                                },
                                status=status.HTTP_200_OK)
                    else:
                        a = DocAdjunto.objects.create(
                            user=user_,
                            tipo=doctipo,
                            tipo_comprobante=tipocomprobante,
                            imagen=nombre_archivo,
                            imagen_url=url,
                            ruta=path)
                else:
                    a = DocAdjunto.objects.create(
                        user=user_,
                        tipo=doctipo,
                        imagen=imagen,
                        imagen_url=url,
                        tipo_comprobante=tipocomprobante)
                id = a.id
                if settings.SITE == "local":
                    url = "{}{}".format(
                          'http://127.0.0.1:8000/media/', a.imagen)
                if settings.SITE not in "local":
                    url = a.imagen_url
            else:
                if settings.USE_S3:
                    url, nombre_archivo, path = upload_s3ine(imagen, username,
                                                            str(tipo))
                    if str(tipo) == '1':
                        valida, informacion = textract_ine(path)
                        validacion, front = validate_information(
                            username, informacion)
                        if validacion is True:
                            a = DocAdjunto.objects.create(
                                user=user_,
                                tipo=doctipo,
                                imagen=nombre_archivo,
                                imagen_url=url,
                                validacion_frontal=front,
                                ruta=path,
                                validado=True)
                        elif validacion is False:
                            fotos = DocAdjunto.objects.filter(
                                user=user_, tipo=doctipo)
                            if len(fotos) < 3:
                                a = DocAdjunto.objects.create(
                                    user=user_,
                                    tipo=doctipo,
                                    imagen=nombre_archivo,
                                    imagen_url=url,
                                    ruta=path)
                                return Response(
                                    {
                                        'Mensaje': "Error al validar "
                                                   "documento volver a "
                                                   "tomar foto"
                                    },
                                    status=status.HTTP_200_OK)
                            elif len(fotos) >= 3:
                                return Response(
                                    {
                                        'Mensaje': front
                                    },
                                    status=status.HTTP_200_OK)
                    if str(tipo) == '2':
                        valida, informacion = textract_ine_reverso(path)
                        validacion, msg = validate_information_ine_back(
                            username, informacion)
                        if validacion is True:
                            a = DocAdjunto.objects.create(
                                user=user_,
                                tipo=doctipo,
                                imagen=nombre_archivo,
                                imagen_url=url,
                                ruta=path,
                                validado=True)
                        elif validacion is False:
                            fotos = DocAdjunto.objects.filter(
                                user=user_, tipo=doctipo)
                            if len(fotos) < 3:
                                a = DocAdjunto.objects.create(
                                    user=user_,
                                    tipo=doctipo,
                                    imagen=nombre_archivo,
                                    imagen_url=url,
                                    ruta=path)
                                return Response(
                                    {
                                        'Mensaje': "Error al validar "
                                                   "documento "
                                                   "volver a tomar foto"
                                    },
                                    status=status.HTTP_200_OK)
                            elif len(fotos) >= 3:
                                return Response(
                                    {
                                        'Mensaje': msg
                                    },
                                    status=status.HTTP_200_OK)
                else:
                    a = DocAdjunto.objects.create(user=user_,
                                                  tipo=doctipo,
                                                  imagen=imagen,
                                                  imagen_url=url)
                if settings.SITE == "local":
                    url = "{}{}".format(
                        'http://127.0.0.1:8000/', a.imagen.url)
                if settings.SITE not in ["local"]:
                    url = a.imagen_url
                id = a.id
        except Exception as ex:
            msg = f"[ImageDoc POST] Error al subir image a bucket: {ex}"
            db_logger.warning(msg)
            return Response(
                {
                    'error': "No fue posible crear el documento"
                },
                status=status.HTTP_200_OK)

        return Response({
            'id': id,
            'user': request.data['user'],
            'tipo': request.data['tipo'],
            'imagen': url},
            status=status.HTTP_200_OK)
