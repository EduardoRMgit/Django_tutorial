from demograficos.serializers import ImageDocSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from demograficos.models import (DocAdjunto,
                                 DocAdjuntoTipo,
                                 TipoComprobante)
import boto3
from django.conf import settings
import os


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
        client.upload_fileobj(archivo,
            settings.AWS_STORAGE_BUCKET_NAME,
            file_path)
        file_url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
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
        client.upload_fileobj(archivo,
            settings.AWS_STORAGE_BUCKET_NAME,
            file_path)
        file_url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
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
        client.upload_fileobj(archivo,
            settings.AWS_STORAGE_BUCKET_NAME,
            file_path)
        file_url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
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
        client.upload_fileobj(archivo,
            settings.AWS_STORAGE_BUCKET_NAME,
            file_path)
        file_url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
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
        client.upload_fileobj(archivo,
            settings.AWS_STORAGE_BUCKET_NAME,
            file_path)
        file_url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
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
        client.upload_fileobj(archivo,
            settings.AWS_STORAGE_BUCKET_NAME,
            file_path)
        file_url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
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
                if settings.SITE == "local":
                    url = "{}{}".format(
                          'http://127.0.0.1:8000/media/', a.imagen)
                if settings.SITE not in "local":
                    url = a.imagen
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
