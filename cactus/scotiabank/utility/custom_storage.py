from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class PrivateStorage(S3Boto3Storage):
    bucket_name = 'scotia-reportes'
    location = 'Comprobantes'


class MediaStorage(S3Boto3Storage):
    bucket_name = 'scotia-reportes'
    if settings.SITE == "prod":
        location = 'ArchivosScotiabankPorEnviar'
    elif settings.SITE == "test":
        location = 'ArchivosScotiabankTest'
    elif settings.SITE == "stage":
        location = 'ArchivosScotiabankStaging'
