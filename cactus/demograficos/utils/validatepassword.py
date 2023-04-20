import re


def PasswordValidator(password):
    valida = ("^(?!.(.)\1\1)(?!.(?:012|123|234|345|456|567|678|789))(?=.[A-Za-z])(?=.\d)(?=.*[%@#!+])[A-Za-z\d%@#!+]{8,}$") # noqa
    if not re.search(valida, password):
        raise Exception("La contraseña no tiene lo solicitado")
