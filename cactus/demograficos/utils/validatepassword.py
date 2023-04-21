import re


def password_validation(password):
    regex = r"^(?!.*(.)\1\1)(?!.*(012|123|234|345|456|567|678|789|987|876|765|654|543|321|210))(?=.*[A-Za-z])(?=.*\d)(?=.*[%@#!+\$])[A-Za-z\d%@#!+\$]{8,}$"  # noqa: E501
    valida = re.match(regex, password)
    if valida:
        return valida
