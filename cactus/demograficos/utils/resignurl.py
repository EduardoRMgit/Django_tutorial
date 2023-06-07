import boto3


def resigned_url(path):
    from cactus.settings import (AWS_ACCESS_KEY_ID,
                                 AWS_SECRET_ACCESS_KEY,
                                 AWS_S3_REGION_NAME,
                                 AWS_STORAGE_BUCKET_NAME)

    client = boto3.client(
        's3',
        config=boto3.session.Config(signature_version='s3v4'),
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_S3_REGION_NAME)

    file_url = client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': AWS_STORAGE_BUCKET_NAME,
            'Key': path,
            'ResponseContentType': 'image/jpeg'
        },
        ExpiresIn=1440,
        HttpMethod=None)
    return file_url
