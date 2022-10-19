import json
import base64

from Crypto.Cipher import AES
from cactus.settings import DAPP_SECRET
from dapp.utility import dapp_secret_


key = dapp_secret_(DAPP_SECRET)


def aes():
    aesCipher = AES.new(
        key,
        AES.MODE_GCM
    )
    nonce = str(aesCipher.nonce.decode('all-escapes'))
    nonce = nonce.replace('\\x', '')
    return nonce, aesCipher


def gcm(body, aesCipher):
    body = json.dumps(body)
    body = "b'{}'".format(body)
    body = eval(body)
    ciphertext, authTag = aesCipher.encrypt_and_digest(body)
    authTag = base64.b64encode(authTag).decode()
    return ciphertext, authTag


def desifrador(nonce, data, authTag):
    aesCipher = AES.new(key, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(data, authTag)
    return plaintext
