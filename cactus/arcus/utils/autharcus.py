from datetime import datetime, timedelta
from django.conf import settings
import pytz
import jwt


def headers_arcus(uid):
    autorizacion = settings.API_KEY_ARCUS
    key = settings.SECRET_ARCUS
    uid = uid
    content = "application/json"
    actual = (datetime.now(pytz.timezone("GMT"))).timestamp()
    expiracion = (
        datetime.now(pytz.timezone("GMT")) + timedelta(minutes=15)).timestamp()
    accept = "application/vnd.regalii.v4.1+json"
    payload = {'sub': autorizacion,
               'exp': int(expiracion),
               'iat': int(actual),
               'jti': "ec2a0bb7-deac-4c21-9ed1-042e3fe58475"}
    bearer = jwt.encode(payload=payload, key=key, algorithm="HS256")
    headers = {'Content-Type': content,
               'Accept': accept,
               'Authorization': f'Bearer {bearer}',
               'Idempotency-Key': "ec2a0bb7-deac-4c21-9ed1-042e3fe58475"}
    return headers
