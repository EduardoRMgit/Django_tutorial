from datetime import datetime, timedelta
from django.conf import settings
import pytz
import jwt


def headers_arcus(uid):
    autorizacion = settings.API_KEY_ARCUS
    key = settings.SECRET_ARCUS
    content = "application/json"
    actual = (datetime.now(pytz.timezone("GMT"))).timestamp()
    expiracion = (
        datetime.now(pytz.timezone("GMT")) + timedelta(minutes=15)).timestamp()
    accept = "application/vnd.regalii.v4.1+json"
    payload = {'sub': autorizacion,
               'exp': int(expiracion),
               'iat': int(actual),
               'jti': uid}
    bearer = jwt.encode(payload=payload, key=key, algorithm="HS256")
    headers = {'Content-Type': content,
               'Accept': accept,
               'Authorization': f'Bearer {bearer}',
               'Idempotency-Key': uid}
    return headers
