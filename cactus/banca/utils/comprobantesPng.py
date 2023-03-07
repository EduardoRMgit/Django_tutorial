import os
import cv2
from PIL import Image
from banca.models import Comprobante, Transaccion
from cactus.settings import MEDIA_ROOT


class CompTrans(object):
    def __init__(self, trans: Transaccion):
        self._trans = trans
        self._tipo = trans.tipoTrans
        self._tp = Comprobante.objects.get(tipo=self._tipo).template
        self._dir = os.path.abspath(os.path.join(MEDIA_ROOT, self._tp.name))
        self._tp = cv2.imread(self._dir)

    def inguz(self, show=False):

        trans = self._trans

        alias = trans.user.Uprofile.alias
        avatar = trans.user.Uprofile.avatar
        monto = round(float(trans.monto), 2)
        fecha = trans.fechaValor.strftime("%m/%d/%Y")
        hora = trans.fechaValor.strftime("%H:%M:%S")
        concepto = trans.concepto
        print(trans.user.username, monto, fecha, hora, concepto)

        # instance = self._trans

        lista = [concepto, trans.claveRastreo, fecha, hora, monto, alias]

        img = cv2.imread(self._dir)
        coord = [
            (118, 408),
            (116, 513),
            (118, 620),
            (119, 725),
            (385, 407),
            (385, 514),
        ]
        for i in range(len(lista)):
            texto = str(lista[i])
            ubicacion = coord[i]
            font = cv2.FONT_ITALIC
            tamañoLetra = 1
            colorLetra = (35, 82, 50)
            grosorLetra = 2

            cv2.putText(
                img,
                texto,
                ubicacion,
                font,
                tamañoLetra,
                colorLetra,
                grosorLetra
            )

        # ComprobanteUsuario.objects.create(transaccion=trans, img=img1)
        cv2.imwrite("hojainguz.jpg", img)
        img1 = Image.open("hojainguz.jpg")
        img2 = Image.open(avatar.avatar_min)
        img1.paste(img2, (1, 1))
        sha = img1
        # if show:

        sha.save("otroreciboinguz.jpg", "JPEG")
        comp_img = open("otroreciboinguz.jpg", "rb")
        os.remove("hojainguz.jpg")
        os.remove("otroreciboinguz.jpg")
        sha.show()
        return comp_img

    def cobro(self):
        trans = self._trans

        alias = trans.user.Uprofile.alias
        monto = round(float(trans.monto), 2)
        fecha = trans.fechaValor.strftime("%m/%d/%Y")
        hora = trans.fechaValor.strftime("%H:%M:%S")
        concepto = trans.concepto
        print(alias, monto, fecha, hora, concepto)

        # instance = self._trans

        lista = [concepto, trans.claveRastreo, fecha, hora, monto, alias]

        img = cv2.imread(self._dir)
        coord = [
            (118, 408),
            (116, 513),
            (118, 620),
            (119, 725),
            (385, 407),
            (385, 514),
        ]
        for i in range(len(lista)):
            texto = str(lista[i])
            ubicacion = coord[i]
            font = cv2.FONT_ITALIC
            tamañoLetra = 1
            colorLetra = (35, 82, 50)
            grosorLetra = 2

            cv2.putText(
                img,
                texto,
                ubicacion,
                font,
                tamañoLetra,
                colorLetra,
                grosorLetra
            )

        # ComprobanteUsuario.objects.create(transaccion=trans, img=img1)
        cv2.imwrite("hoja.jpg", img)
        img1 = Image.open("hoja.jpg")
        # img2 = Image.open("banca/OTROSBANCOS.png")
        # img1.paste(img2, (650, 300), mask=img2)
        sha = img1
        # if show:
        #     sha.show()
        sha.save("otrorecibo.jpg", "JPEG")
        comp_img = open("otrorecibo.jpg", "rb")
        sha.show()
        os.remove("hoja.jpg")
        os.remove("otrorecibo.jpg")

        return comp_img

    def cobroL(self, cobro):
        pass

    def stp(self):
        trans = self._trans
        usertrans = trans.user.username
        alias = trans.user.Uprofile.alias
        avatar = trans.user.Uprofile.avatar

        monto = round(float(trans.monto), 2)
        fecha = trans.fechaValor.strftime("%m/%d/%Y")
        hora = trans.fechaValor.strftime("%H:%M:%S")
        concepto = trans.concepto
        print(usertrans, monto, fecha, hora, concepto)

        # instance = self._trans

        lista = [concepto, trans.claveRastreo, fecha, hora, monto, alias]

        img = cv2.imread(self._dir)
        coord = [
            (118, 408),
            (116, 513),
            (118, 620),
            (119, 725),
            (385, 407),
            (385, 514),
        ]  # noqa: E501
        for i in range(len(lista)):
            texto = str(lista[i])
            ubicacion = coord[i]
            font = cv2.FONT_ITALIC
            tamañoLetra = 1
            colorLetra = (35, 82, 50)
            grosorLetra = 2

            cv2.putText(
                img,
                texto,
                ubicacion,
                font,
                tamañoLetra,
                colorLetra,
                grosorLetra
            )  # noqa: E501

        # ComprobanteUsuario.objects.create(transaccion=trans, img=img1)
        cv2.imwrite("hojastp.jpg", img)
        img1 = Image.open("hojastp.jpg")
        print(trans.user)
        print("****************************************************")
        img2 = Image.open(avatar.avatar_img)
        img1.paste(img2, (1, 1))
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        sha = img1

        # if show:
        #     sha.show()
        sha.save("otrorecibostp.jpg", "JPEG")
        comp_img = open("otrorecibostp.jpg", "rb")
        sha.show()
        os.remove("hojastp.jpg")
        os.remove("otrorecibostp.jpg")

        return comp_img

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

    def trans(self):
        print(self._tipo.codigo)
        if self._tipo.codigo == "18":

            return self.inguz()
        if self._tipo.codigo == "20":
            return self.cobro()

        if self._tipo.codigo == "2":
            return self.stp()
