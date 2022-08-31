def _calcula_fecha_condensada(fecha):

    """
    Devuelve una lista que contiene 4 enteros que corresponden a la fecha
    en forma condensada.
    """
    a = (fecha.year - 2013) * 372
    b = (fecha.month - 1) * 31
    c = fecha.day - 1
    r = a + b + c
    res = list(str(r).zfill(4))
    return res


def _calcula_importe_condensado(importe):

    """

    Devuelve un entero correspondiente al importe en forma condensada.

    """
    lista = list(str(importe))
    lista.reverse()
    ponderador = (7, 3, 1)
    sum = 0
    for i, v in enumerate(lista):
        if v.isdigit():
            digito = int(v)
            sum += digito * ponderador[i % len(ponderador)]
    res = sum % 10
    return res


def _convierte_todo_a_valor(lista):

    """

    Recibe una lista de caracteres alfanuméricos y devuelve otra lista
    con todos los elementos recibidos convertidos a valores numéricos
    basándose en equivalencias predefinidas.

    """
    for i, v in enumerate(lista):
        if v.isalpha():
            valor = int(ord(v.upper()) - ord('A')) // 3 + 2
            lista[i] = str(valor)
        lista[i] = int(lista[i])
    return lista


def _calcula_digitos_verificadores(valores):

    """

    Devuelve un string de longitud 2, que corresponde a los dígitos
    verificadores de la entrada recibida.

    """
    valores.reverse()
    ponderador = (11, 13, 17, 19, 23)
    sum = 0
    for i, v in enumerate(valores):
        sum += v * ponderador[i % len(ponderador)]
    r = sum % 97 + 1
    r_str = str(r).zfill(2)
    return r_str


def genera_linea_de_captura(referencia,
                            fecha_limite_pago,
                            importe,
                            constante):

    """

    Calcula y devuelve un string con la línea de captura correspondiente

    a los datos proporcionados.


        Parámetros:

            -- referencia (str): String sin restricción en la longitud.

            -- fecha_limite_pago (date): Objeto de tipo datetime.date que

               indica la fecha límite de pago.

            -- importe (float | str): Indica el importe a pagar.

            -- constante (int | str): Un dígito restringido a los números del 0

               al 6 ó alguna de las siguientes letras: A, B, C, D, E, X, Y, Z.
        Valor de retorno:

            -- linea_captura (str): String con la línea de captura completa.

    """

    referencia_lst = list(str(referencia))
    fecha_condensada_lst = _calcula_fecha_condensada(fecha_limite_pago)
    importe_condensado = _calcula_importe_condensado(importe)
    ref_fec_imp_con = referencia_lst + \
                      fecha_condensada_lst + \
                      [str(importe_condensado)] + \
                      [str(constante)]
    valores = _convierte_todo_a_valor(ref_fec_imp_con)
    valores_copia = valores.copy()
    digitos_verificadores = _calcula_digitos_verificadores(valores_copia)
    valores_str = [str(v) for v in valores]
    linea_captura = ''.join(valores_str) + digitos_verificadores
    return linea_captura
