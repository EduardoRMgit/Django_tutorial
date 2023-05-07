import requests
from datetime import datetime
import hashlib
import hmac
import base64
import pytz

date = datetime.now(tz=pytz.utc).astimezone(pytz.timezone('GMT'))
date = date.strftime('%a, %d %b %Y %H:%M:%S GMT')
autorizacion = "00c0d2159be9988bfb4d5fd36a6d97df"
key = "+8teRHyPKfD5N/EWiRxeWsaDwjtD+ybdgZ0yeo8PtEkhV03cEUFTYxUD6AshGXqfgm/WkNbL6LY+nyI7y9ifJw=="
content = "application/json"
content_md5 = ""
accept = "application/vnd.regalii.v3.mx+json"
checksum = f"{content},{content_md5},/account,{date}".encode("utf-8")
checksum = (hmac.new(key.encode('utf-8'), checksum, hashlib.sha1)).digest()
checksum = (base64.b64encode(checksum)).decode("ascii")
headers = {'Content-Type': content,
           'Accept': accept,
           'Date': date,
           'Authorization': f'APIAuth {autorizacion}:{checksum}'
}
checksum = f"{content},{content_md5},/billers/utilities,{date}".encode("utf-8")
checksum = (hmac.new(key.encode('utf-8'), checksum, hashlib.sha1)).digest()
checksum = (base64.b64encode(checksum)).decode("ascii")
headers2 = {'Content-Type': content,
           'Accept': accept,
           'Date': date,
           'Authorization': f'APIAuth {autorizacion}:{checksum}'}
response = requests.get(url='https://api.staging.arcusapi.com/account', headers=headers)
response2 = requests.get(url='https://api.staging.arcusapi.com/billers/utilities', headers=headers2)
print(response)
print(response._content)
print(response2)
print(response2._content)
