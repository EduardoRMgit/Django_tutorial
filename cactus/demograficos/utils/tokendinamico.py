import random
from demograficos.models import TokenDinamico
from datetime import timedelta
from django.utils import timezone


def tokenD(user):
    token = random.randint(1000000000, 9999999999)
    tokenv = TokenDinamico.objects.filter(token=token).count()
    while tokenv > 0:
        token = random.randint(1000000000, 9999999999)
        tokenv = TokenDinamico.objects.filter(token=token).count()
    token = TokenDinamico.objects.create(user=user, token=token)
    return token


def validaToken(user, token_d):
    try:
        token = TokenDinamico.objects.filter(user=user, token=token_d)
        hoy = timezone.now()
        tokensc = token.count()
        if tokensc:
            comparacion = (hoy - token.last().fecha < timedelta(minutes=2))
            print(comparacion, "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
            if comparacion:
                token.delete()
                return True
        else:
            token.delete()
            return False
    except Exception as ex:
        raise Exception("Fallo al validar token", ex)
