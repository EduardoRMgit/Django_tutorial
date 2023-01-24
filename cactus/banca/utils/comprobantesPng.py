import os
import cv2
from PIL import Image
from banca.models import Comprobante
from cactus.settings import MEDIA_ROOT


class CompTrans(object):

    def __init__(self, tipo):
        self._tipo = tipo
        self._tp = Comprobante.objects.get(tipo__codigo=self._tipo).template
        self._dir = os.path.abspath(os.path.join(MEDIA_ROOT, self._tp.name))
        self._tp = cv2.imread(self._dir)

    def inguz(self, trans):
        alias = trans.user.Uprofile.alias
        monto = round(float(trans.monto), 2)
        fecha = trans.fechaValor.strftime("%m/%d/%Y")
        hora = trans.fechaValor.strftime("%H:%M:%S")
        concepto = trans.inguztransaction.concepto
        print(
            alias,
            monto,
            fecha,
            hora,
            concepto
        )

    def cobro(cobro):
        pass

    def cobroL(self, cobro):
        pass

    def stp(self, stp):
        pass

    def spei(self, trans):
        pass

    def scotiaD(self, scotia):
        pass

    def scotiaR(self, scotia):
        pass

    def soporte(self, ticket):
        pass

    def cancelacion(self, info):
        pass
