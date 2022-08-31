from storages.backends.s3boto3 import S3Boto3Storage


class PrivateStorage(S3Boto3Storage):
    bucket_name = 'scotia-reportes'
    location = 'Comprobantes'


class MediaStorage(S3Boto3Storage):
    bucket_name = 'scotia-reportes'
    # location = 'ArchivosScotiabankEnviados'
    location = 'ArchivosScotiabankPorEnviar'
