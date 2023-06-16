import boto3
import os


def upload_arcus(path, doc):

    from cactus.settings import (AWS_ACCESS_KEY_ID,
                                 AWS_SECRET_ACCESS_KEY,
                                 AWS_S3_REGION_NAME,
                                 AWS_STORAGE_BUCKET_NAME)

    file_path = os.path.join('arcus/', path)

    client = boto3.client(
        's3',
        config=boto3.session.Config(signature_version='s3v4'),
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_S3_REGION_NAME)
    client.put_object(Body=doc, Bucket=AWS_STORAGE_BUCKET_NAME, Key=file_path)
