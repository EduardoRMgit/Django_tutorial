from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class StaticStorage(S3Boto3Storage):
    location = settings.AWS_LOCATION
    default_acl = 'public-read'


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False

    def get_object_parameters(self, name):

        params = {
            "ServerSideEncryption": "AES256"
        }

        params.update(self.object_parameters.copy())

        return params
