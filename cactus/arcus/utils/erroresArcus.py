

def mensajes_error(requests):

    if requests['code'] == 'R100':
        mensaje = ("La solicitud no ha podido ser procesada, "
                   "intenta de nuevo en unas horas.")
    elif requests['code'] == 'R2':
        mensaje = ("La referencia numérica capturada no existe, "
                   "revisa los datos ingresados.")
    elif requests['code'] == 'R7':
        mensaje = ('La referencia numérica no acepta este tipo de pagos.')
    elif requests['code'] == 'R11':
        mensaje = ('La referencia numérica no acepta pagos parciales.')
    elif requests['code'] == 'R15':
        mensaje = ('La referencia numérica no presenta deuda.')
    elif requests['code'] == 'R16':
        mensaje = ('No se ha podido consultar la referencia, '
                   'intenta más tarde.')
    elif requests['code'] == 'R19':
        mensaje = ('Lo sentimos, la compañía seleccionada no está '
                   'recibiendo pagos.')
    elif requests['code'] == 'R22':
        mensaje = ('Lo sentimos, la compañía seleecionada está '
                   'en mantenimiento')
    elif requests['code'] == 'R24':
        mensaje = ('La solicitud de pago ha sobrepasado el tiempo '
                   'de espera, inteta más tarde')
    elif requests['code'] == 'R36':
        mensaje = ('Su proovedor ha declinado el pago, intente más tarde')
    elif requests['code'] == 'R99':
        mensaje = ('La solicitud no ha podido ser procesada, intenta '
                   'de nuevo en unas horas')
    return mensaje
