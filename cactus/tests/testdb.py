from django.core.management import call_command
from .perms import load_groups


def load_min_test():
    call_command('loaddata', 'nivelCuenta', verbosity=0)
    call_command('loaddata', 'customer', verbosity=0)
    call_command('loaddata', 'adminUtils', verbosity=0)
    load_groups()
    call_command('loaddata', 'urls', verbosity=0)
    call_command('loaddata', 'user', verbosity=0)
    call_command('loaddata', 'tipoAnual', verbosity=0)
    call_command('loaddata', 'statusTrans', verbosity=0)
    call_command('loaddata', 'tipoTransaccion', verbosity=0)
    call_command('loaddata', "cami", verbosity=0)
    call_command('loaddata', 'comision', verbosity=0)
    call_command('loaddata', 'carProducto', verbosity=0)
    call_command('loaddata', 'institucion', verbosity=0)
    call_command('loaddata', 'errorestransaccion', verbosity=0)
    call_command('loaddata', 'paisesDisponibles', verbosity=0)
    call_command('loaddata', 'transaccion', verbosity=0)
    call_command('loaddata', 'statusRegistro', verbosity=0)
