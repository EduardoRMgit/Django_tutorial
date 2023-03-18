import os
import cv2
from PIL import Image
from banca.models import Comprobante, Transaccion
from spei.models import StpTransaction
from cactus.settings import MEDIA_ROOT


class CompTrans(object):
    def __init__(self, trans: Transaccion):
        self._trans = trans
        self._tipo = trans.tipoTrans
        codigo = self._tipo.codigo
        status = trans.statusTrans.nombre
        print((status))
        print(codigo)
        if status == "exito":
            codigo = codigo
        if status == "rechazada":
            codigo = int(codigo)
            codigo += 1
            codigo = str(codigo)
        else:
            pass
        print(codigo, 'cooooooooodigo')
        self._tp = Comprobante.objects.get(codigo=codigo).template
        self._dir = os.path.abspath(os.path.join(MEDIA_ROOT, self._tp.name))
        self._tp = cv2.imread(self._dir)

    def inguz(self, show=False):
        trans = self._trans
        nombre = trans.user.Uprofile.get_nombre_completo()
        alias = trans.user.Uprofile.alias
        avatar = trans.user.Uprofile.avatar
        monto = round(float(trans.monto), 2)
        fecha = trans.fechaValor.strftime("%m/%d/%Y")
        hora = trans.fechaValor.strftime("%H:%M:%S")
        concepto = trans.concepto
        print(trans.user.username, monto, fecha, hora, concepto)

        # instance = self._trans

        lista = [nombre, concepto, alias,
                 fecha, hora, monto, trans.claveRastreo]
        

        img = cv2.imread(self._dir)
        coord = [
            (220, 350),
            (119, 725),
            (385, 514),
            (119, 620),
            (385, 620),
            (119, 513),
            (119, 805),
        ]
        if trans.statusTrans.nombre == 'rechazada':
            lista.remove(lista[-1])
            coord.remove(coord[-1])
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
        avatar = os.path.abspath(os.path.join(
            MEDIA_ROOT, avatar.avatar_img.name))
        avatar = cv2.imread(avatar, -1)
        avatar = cv2.resize(avatar, (250, 250))
        x_offset = 180
        y_offset = 0
        y1, y2 = y_offset, y_offset + avatar.shape[0]
        x1, x2 = x_offset, x_offset + avatar.shape[1]
        alpha_s = avatar[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s
        for c in range(0, 3):
            img[y1:y2, x1:x2, c] = (alpha_s * avatar[:, :, c] +
                                    alpha_l * img[y1:y2, x1:x2, c])

        # if show:
        img_name = "comprobanteInguz.jpg"
        cv2.imwrite(img_name, img)
        comp_img = open(img_name, "rb")
        os.remove(img_name)
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
        nombre = trans.user.Uprofile.get_nombre_completo()
        importe = "${:,.2f}".format(round(float(trans.monto), 2))
        fecha = trans.fechaValor.strftime("%m/%d/%Y")
        hora = trans.fechaValor.strftime("%H:%M:%S")
        concepto = trans.concepto
        cuenta = f"*{trans.user.Uprofile.cuentaClabe[13:-1]}"
        rastreo = trans.claveRastreo
        referencia = StpTransaction.objects.get(
            transaccion=trans).referenciaNumerica

        fields = [
            [nombre,   (112,  386), 2, 0.9, (0, 0, 0), 1, 16],
            [importe,  (112,  490), 2, 1.0, (0, 0, 0), 2, 16],
            [cuenta,   (378,  490), 2, 0.9, (0, 0, 0), 1, 16],
            [fecha,    (112,  590), 2, 0.9, (0, 0, 0), 1, 16],
            [hora,     (378,  590), 2, 0.9, (0, 0, 0), 1, 16],
            [concepto, (112,  690), 2, 0.9, (0, 0, 0), 1, 16],
        ]
        if trans.statusTrans.nombre == 'exito':
            field_ = [
                [rastreo,  (112, 800), 2, 0.9, (0, 0, 0), 1, 16],
                [referencia, (112, 900), 2, 0.9, (0, 0, 0), 1, 16],
            ]
            for field in field_:
                fields.append(field)
            print(fields, 'a')

        img = cv2.imread(self._dir)
        for field in fields:
            cv2.putText(img, *field)
        img_name = "comprobanteSTP.jpg"
        cv2.imwrite(img_name, img)
        comp_img = open(img_name, "rb")
        os.remove(img_name)
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
        if self._tipo.codigo == "18":

            return self.inguz()
        if self._tipo.codigo == "20":
            return self.cobro()

        if self._tipo.codigo == "2":
            return self.stp()
