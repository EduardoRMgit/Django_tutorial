from functools import reduce


def CuentaClabe(user_id):
    string_length = len(str(user_id))
    spacios_faltantes = 7 - string_length
    string_espacios = "0" * spacios_faltantes
    cuentaBase = "{}{}".format(string_espacios, user_id)
    cuenta = list(map(int, str(cuentaBase)))

    # prefijo = [6, 4, 6, 1, 8, 0, 1, 9, 0, 0]
    prefijo = [6, 4, 6, 1, 8, 0, 2, 1, 8, 0]
    cuentaBase = prefijo + cuenta
    ponderacion = [3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7]

    paso1 = list(map(lambda x, y: x*y, cuentaBase, ponderacion))
    paso2 = list(map(lambda x: x % 10, paso1))
    paso3 = reduce(lambda x, y: x+y, paso2)
    paso4 = paso3 % 10
    paso5 = 10 - paso4
    paso6 = paso5 % 10
    cuentaBase.append(paso6)
    cuentaClabe = cuentaBase

    cuentaClabeStringList = list(map(lambda x: str(x), cuentaClabe))
    cuentaClabeString = "".join(cuentaClabeStringList)

    return cuentaClabeString
