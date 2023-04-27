import random
from demograficos.models import TokenDinamico
from datetime import timedelta
from django.utils import timezone


def tokenD(user):
    token = random.randint(1000000000, 9999999999)
    tokenv = TokenDinamico.objects.filter(token=token).count()
    if tokenv:
        token = random.randint(1000000000, 9999999999)
    TokenDinamico.objects.create(user, token=token)
    return token


def validaToken(token_d):
    token = TokenDinamico.objects.filter(token=token_d)
    hoy = timezone.now()
    tokensc = token.count()
    if tokensc:
        comparacion = (hoy - token.fecha > timedelta(minutes=2))
        if comparacion:
            token.delete()
            return True
    else:
        return False
