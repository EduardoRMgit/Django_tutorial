from pyotp import TOTP


def tokenD():
    key = b'NRXXC5LFONSWC==='
    token = TOTP(key, interval=20)
    return token
