from scotiabank.models import ScotiaTransferencia
from scotiabank.utility.ScotiaUtil import GeneraTransferencia


def run():

    movimientos = ScotiaTransferencia.objects.filter(statusTrans=0)
    if movimientos.count() > 0:
        GeneraTransferencia(movimientos)
    else:
        pass
