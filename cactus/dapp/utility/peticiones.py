import requests
import base64
import time

from cactus.settings import DAPP_KEY

from dapp.utility.encripcion import aes, gcm


class Peticiones:
    def __init__(self):
        self.url = 'https://wallets-sandbox.dapp.mx/v2/'
        tk = "b'{}'".format(DAPP_KEY)
        tk = eval(tk)
        tk = base64.b64encode(tk)
        tk = tk.decode("utf-8")
        self.headers = {'Authorization': 'Basic ' + tk}

    def paymentInfo(self, qr):
        urlComplement = 'dapp-codes/{}'.format(
            qr
        )
        url = self.url + urlComplement
        authorization = requests.get(
            url,
            headers=self.headers)
        return authorization

    def payments(self, **kwargs):
        if 'id' in kwargs:
            url = 'id={}'.format(
                kwargs['id']
            )
        if 'reference' in kwargs:
            url = 'reference={}'.format(
                kwargs['reference']
            )
        if 'id' in kwargs and 'reference' in kwargs:
            url = 'id={}&reference={}'.format(
                kwargs['id'], kwargs['reference']
            )
        urlComplement = 'payments?{}'.format(
            url
        )
        url = self.url + urlComplement
        authorization = requests.get(
            url,
            headers=self.headers
        )
        return authorization

    def storeInfo(self, **kwargs):
        urlComplement = 'stores?latitude={}&longitude={}'.format(
            kwargs['latitude'], kwargs['longitude']
        )
        if 'radio' in kwargs:
            urlComplement = '{}&radio={}'.format(
                urlComplement,
                kwargs['radio']
            )
        url = self.url + urlComplement
        authorization = requests.get(
            url,
            headers=self.headers)
        return authorization

    def createPayment(self, **kwargs):
        urlComplement = 'payments/'
        url = self.url + urlComplement
        nonce, aesCipher = aes()
        body = {}
        data = {}
        if 'name' in kwargs:
            data['name'] = kwargs['name']
        if 'mail' in kwargs:
            data['mail'] = kwargs['mail']
        if 'phone' in kwargs:
            data['phone'] = kwargs['phone']
        if 'reference' in kwargs:
            data['reference'] = kwargs['reference']
        if 'cash_amount' in kwargs:
            data['cash_amount'] = kwargs['cash_amount']
        data['amount'] = kwargs['amount']
        data['code'] = kwargs['code']
        data['description'] = kwargs['description']
        body['timestamp'] = int(time.time())
        body['nonce'] = nonce
        body['data'] = data
        ciphertext, authTag = gcm(body, aesCipher)
        header = self.headers
        header['mac'] = authTag
        header['nonce'] = nonce
        header['Content-Type'] = 'text/plain'
        ciphertext = base64.b64encode(ciphertext)
        ciphertext = ciphertext.decode('utf-8')
        pago = requests.post(
            url,
            headers=header,
            data=ciphertext
        )
        return pago
