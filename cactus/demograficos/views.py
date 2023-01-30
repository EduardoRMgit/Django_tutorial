from demograficos.serializers import ImageDocSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from demograficos.models import (DocAdjunto,
                                 DocAdjuntoTipo,
                                 TipoComprobante)
import pytesseract
from PIL import Image
from pytesseract import Output
import io
import requests
import datetime
from demograficos.utils.meses import meses
from demograficos.utils.dates import normalizeDates
import re
import os
import boto3
from django.conf import settings


def upload_s3_docs(tipocomprobante, archivo, user):
    from cactus.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    if tipocomprobante == '1':
        nombre_archivo = f"comprobante_cfe_{user}"
        directory = 'cfe'
        file_path = os.path.join(
            directory,
            nombre_archivo
        )
        file_path = os.path.join('docs/docs/comprobantes', file_path)
        client = boto3.client(
            's3',
            config=boto3.session.Config(signature_version='s3v4'),
            aws_acces_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name="us-east-2")
        client.upload_fileobj(archivo, "phototest420", file_path)
        file_url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': "phototest420",
                'Key': file_path
            },
            ExpiresIn=1440,
            HttpMethod=None)
    elif tipocomprobante == '2':
        nombre_archivo = f"comprobante_telmex_{user}"
        directory = 'telmex'
        file_path = os.path.join(
            directory,
            nombre_archivo
        )
        file_path = os.path.join('docs/docs/comprobantes', file_path)
        client = boto3.client(
            's3',
            config=boto3.session.Config(signature_version='s3v4'),
            aws_acces_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name="us-east-2")
        client.upload_fileobj(archivo, "phototest420", file_path)
        file_url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': "phototest420",
                'Key': file_path
            },
            ExpiresIn=1440,
            HttpMethod=None)
    elif tipocomprobante == '3':
        nombre_archivo = f"comprobante_izzi_{user}"
        directory = 'izzi'
        file_path = os.path.join(
            directory,
            nombre_archivo
        )
        file_path = os.path.join('docs/docs/comprobantes', file_path)
        client = boto3.client(
            's3',
            config=boto3.session.Config(signature_version='s3v4'),
            aws_acces_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name="us-east-2")
        client.upload_fileobj(archivo, "phototest420", file_path)
        file_url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': "phototest420",
                'Key': file_path
            },
            ExpiresIn=1440,
            HttpMethod=None)
    elif tipocomprobante == '4':
        nombre_archivo = f"comprobante_totalplay_{user}"
        directory = 'totalplay'
        file_path = os.path.join(
            directory,
            nombre_archivo
        )
        file_path = os.path.join('docs/docs/comprobantes', file_path)
        client = boto3.client(
            's3',
            config=boto3.session.Config(signature_version='s3v4'),
            aws_acces_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name="us-east-2")
        client.upload_fileobj(archivo, "phototest420", file_path)
        file_url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': "phototest420",
                'Key': file_path
            },
            ExpiresIn=1440,
            HttpMethod=None)
    return file_url


def upload_s3ine(archivo, user, tipo):
    from cactus.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    if tipo == "1":
        nombre_archivo = f"ine_frontal_{user}"
        directory = 'ine'
        file_path = os.path.join(
            directory,
            nombre_archivo
        )
        file_path = os.path.join('docs/docs/', file_path)
        client = boto3.client(
            's3',
            config=boto3.session.Config(signature_version='s3v4'),
            aws_acces_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name="us-east-2")
        client.upload_fileobj(archivo, "phototest420", file_path)
        file_url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': "phototest420",
                'Key': file_path
            },
            ExpiresIn=1440,
            HttpMethod=None)
    elif tipo == "2":
        nombre_archivo = f"ine_reverso_{user}"
        directory = 'ineReverso'
        file_path = os.path.join(
            directory,
            nombre_archivo
        )
        file_path = os.path.join('docs/docs/', file_path)
        client = boto3.client(
            's3',
            config=boto3.session.Config(signature_version='s3v4'),
            aws_acces_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name="us-east-2")
        client.upload_fileobj(archivo, "phototest420", file_path)
        file_url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': "phototest420",
                'Key': file_path
            },
            ExpiresIn=1440,
            HttpMethod=None)
    return file_url


class ImageDoc(generics.CreateAPIView):
    serializer_class = ImageDocSerializer

    def post(self, request):
        imagen = request.data['imagen']
        tipo = request.data['tipo']
        user = request.data['user']
        user_ = User.objects.get(id=user)
        username = user_.username
        doctipo = DocAdjuntoTipo.objects.get(id=tipo)
        reg = r"(0[1-9]|[12][0-9]|3[01])([\/|.|\-|\s])([A-Za-z0-9])+" \
              r"([\/|.|\-|\s])([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])"
        try:
            if request.data['tipo_comprobante'] != '':
                tipo_comprobante = request.data['tipo_comprobante']
                tipocomprobante = TipoComprobante.objects.get(
                    id=tipo_comprobante)
                if settings.USE_S3:
                    url = upload_s3_docs(tipocomprobante, imagen, username)
                    a = DocAdjunto.objects.create(
                        user=user_,
                        tipo=doctipo,
                        imagen=url,
                        tipo_comprobante=tipocomprobante)
                else:
                    a = DocAdjunto.objects.create(
                        user=user_,
                        tipo=doctipo,
                        imagen=imagen,
                        tipo_comprobante=tipocomprobante)
                id = a.id
                if tipo == '3':
                    if settings.SITE == "local":
                        url = "{}{}".format(
                            'http://127.0.0.1:8000/media/', a.imagen)
                    if settings.SITE not in "local":
                        url = a.imagen
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
                            listf.append(text)
                            if re.match(pattern, text):
                                listf.append(text)
                                a = re.match(pattern, text)
                                a = a.group()
                                dates.append(a)
                    if request.data['tipo_comprobante'] == '2':
                        dates = normalizeDates(dates)
                        datesn = []
                        for h in dates:
                            try:
                                if len(h) > 8:
                                    c = datetime.datetime.strptime(
                                        h, "%d-%m-%Y")
                                    datesn.append(c)
                            except Exception as e:
                                print(e)
                        try:
                            a = datesn[0]
                            b = datesn[1]
                        except Exception as e:
                            print(e)
                        try:
                            if b > a:
                                hoy = datetime.datetime.now()
                                comparacion = (hoy - a > datetime.timedelta(
                                    days=90))
                                if comparacion:
                                    return Response({"message":
                                        "comprobante mayor a 3 meses"})
                                else:
                                    return Response({
                                        'id': id,
                                        'user': request.data['user'],
                                        'tipo': request.data['tipo'],
                                        'imagen': url,
                                        'tipo_comprobante': request.data[
                                            'tipo_comprobante'],
                                        'message': "Comprobante Valido",
                                    })
                            elif a > b:
                                hoy = datetime.datetime.now()
                                comparacion = (hoy - b > datetime.timedelta(
                                    days=90))
                                if comparacion:
                                    return Response({"message":
                                        "comprobante mayor a 3 meses"})
                                else:
                                    return Response({
                                        'id': id,
                                        'user': user_,
                                        'tipo': request.data['tipo'],
                                        'imagen': url,
                                        'tipo_comprobante': request.data[
                                            'tipo_comprobante'],
                                        'message': "Comprobante Valido",
                                    })
                        except Exception as e:
                            print(e)
                    elif request.data['tipo_comprobante'] == '3':
                        datesn = []
                        datesh = []
                        for i in dates:
                            try:
                                k = meses(i)
                                datesn.append(k)
                            except Exception as e:
                                print(e)
                        for h in datesn:
                            try:
                                c = datetime.datetime.strptime(h, "%d-%m-%y")
                                datesh.append(c)
                            except Exception as e:
                                print(e)
                        try:
                            a = datesh[0]
                            b = datesh[1]
                        except Exception as e:
                            print(e)
                        hoy = datetime.datetime.now()
                        if a > b:
                            comparacion = (hoy - a > datetime.timedelta(
                                days=90))
                            if comparacion:
                                return Response({
                                    "message": "Comprobante mayor a 3 meses"})
                            else:
                                return Response({
                                    'id': id,
                                    'user': request.data['user'],
                                    'tipo': request.data['tipo'],
                                    'imagen': url,
                                    'tipo_comprobante': request.data[
                                        'tipo_comprobante'],
                                    'message': "Comprobante Valido",
                                })
                        elif b > a:
                            comparacion = (hoy - b > datetime.timedelta(
                                days=90))
                            if comparacion:
                                return Response({
                                    "message": "Comprobante mayor a 3 meses"})
                            else:
                                return Response({
                                    'id': id,
                                    'user': request.data['user'],
                                    'tipo': request.data['tipo'],
                                    'imagen': url,
                                    'tipo_comprobante': request.data[
                                        'tipo_comprobante'],
                                    'message': "Comprobante Valido",
                                })
                    elif request.data['tipo_comprobante'] == '4':
                        datesn = []
                        datesh = []
                        for i in dates:
                            try:
                                k = meses(i)
                                datesn.append(k)
                            except Exception as e:
                                print(e)
                        for i in datesn:
                            try:
                                c = datetime.datetime.strptime(i, "%d/%m/%Y")
                                datesh.append(c)
                            except Exception as e:
                                print(e)
                        hoy = datetime.datetime.now()
                        if len(datesh) >= 2:
                            try:
                                a = datesh[0]
                                b = datesh[1]
                            except Exception as e:
                                print(e, "La lista solo tiene 1 indice")
                        else:
                            a = datesh[0]
                            comparacion = (hoy - a > datetime.timedelta(
                                days=90))
                            if comparacion:
                                return Response({"message":
                                    "comprobante mayor a 3 meses"})
                            else:
                                return Response({
                                    'id': id,
                                    'user': request.data['user'],
                                    'tipo': request.data['tipo'],
                                    'imagen': url,
                                    'tipo_comprobante': request.data[
                                        'tipo_comprobante'],
                                    'message': "Comprobante Valido",
                                })

            else:
                if settings.USE_S3:
                    url = upload_s3ine(imagen, username, doctipo)
                    a = DocAdjunto.objects.create(user=user_,
                                                  tipo=doctipo,
                                                  imagen=url)
                else:
                    a = DocAdjunto.objects.create(user=user_,
                                                  tipo=doctipo,
                                                  imagen=imagen)
                if settings.SITE == "local":
                    url = "{}{}".format(
                        'http://127.0.0.1:8000/media/', a.imagen)
                if settings.SITE not in "local":
                    url = a.imagen
                id = a.id
        except Exception as e:
            print(e)
        return Response({
            'id': id,
            'user': request.data['user'],
            'tipo': request.data['tipo'],
            'imagen': url},
            status=status.HTTP_200_OK)
