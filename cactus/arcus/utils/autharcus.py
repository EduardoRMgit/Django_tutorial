from datetime import datetime
import hashlib
import hmac
import base64
import pytz
from django.conf import settings


def headers_arcus(endpoint):
    date = datetime.now(tz=pytz.utc).astimezone(pytz.timezone('GMT'))
    date = date.strftime('%a, %d %b %Y %H:%M:%S GMT')
    autorizacion = settings.API_KEY_ARCUS
    key = settings.SECRET_ARCUS
    content = "application/json"
    content_md5 = ""
    accept = "application/vnd.regalii.v3.mx+json"
    checksum = f"{content},{content_md5},{endpoint},{date}".encode("utf-8")
    checksum = (hmac.new(key.encode('utf-8'), checksum, hashlib.sha1)).digest()
    checksum = (base64.b64encode(checksum)).decode("ascii")
    headers = {'Content-Type': content,
               'Accept': accept,
               'Date': date,
               'Authorization': f'APIAuth {autorizacion}:{checksum}'}
    return headers
