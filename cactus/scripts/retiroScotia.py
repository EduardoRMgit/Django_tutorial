from scotiabank.models import ScotiaRetiro
from scotiabank.utility.ScotiaUtil import GeneraRetiro


def run():

    movimientos = ScotiaRetiro.objects.filter(statusTrans=0)
    if movimientos.count() > 0:
        GeneraRetiro(movimientos)
    else:
        pass
