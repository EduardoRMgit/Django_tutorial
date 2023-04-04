import boto3
from django.conf import settings


def get_pdf_url(archivo, file_path):
    from cactus.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

    client = boto3.client(
        's3',
        config=boto3.session.Config(signature_version='s3v4'),
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="us-east-1")
    client.upload_fileobj(archivo,
                          settings.AWS_STORAGE_BUCKET_NAME,
                          file_path)
    file_url = client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': file_path,
        },
        ExpiresIn=1440,
        HttpMethod=None)
    return file_url
