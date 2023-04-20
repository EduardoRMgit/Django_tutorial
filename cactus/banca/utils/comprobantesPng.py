import os
import cv2
from banca.models import Comprobante
from spei.models import StpTransaction
from cactus.settings import MEDIA_ROOT
from django.conf import settings
import imutils


class CompTrans(object):
    def __init__(self, trans):
        try:
            self.trans_ = trans
            trans = trans.transaccion.transaccion
        except Exception:
            pass
        self._trans = trans
        self._tipo = self._trans.tipoTrans
        print(self._tipo)
        self._codigo = self._tipo.codigo
        self._status = self._trans.statusTrans.nombre
        if self._status == "exito":
            codigo = self._codigo
        if self._status == "rechazada":
            codigo = int(self._codigo)
            codigo += 1
            codigo = str(codigo)
        self._tp = Comprobante.objects.get(codigo=codigo).template
        self._dir = os.path.abspath(os.path.join(MEDIA_ROOT, self._tp.name))
        self._tp = cv2.imread(self._dir)

    def inguz(self, show=False):
        trans = self._trans
        nombre = trans.user.Uprofile.get_nombre_completo()
        alias = f"@{trans.user.Uprofile.alias}"
        avatar = trans.user.Uprofile.avatar
        monto = str(round(float(trans.monto), 2))
        cuenta = f"*{trans.user.Uprofile.cuentaClabe[13:-1]}"
        fecha = trans.fechaValor.strftime("%m/%d/%Y")
        hora = trans.fechaValor.strftime("%H:%M:%S")
        concepto = trans.concepto

        if settings.SITE == "local":
            avatar = os.path.abspath(os.path.join(
                MEDIA_ROOT, avatar.avatar_img.name))
            avatar = cv2.imread(avatar, -1)
            img = cv2.imread(self._dir)
        elif settings.SITE not in "local":
            avatar = avatar.avatar_img.name
            avatar = imutils.url_to_image(avatar, -1)
            img = imutils.url_to_image(self._dir)
        fields = [
            [nombre,    (210, 350), 2, 0.9, (0, 0, 0), 1, 16],
            [concepto,  (118, 700), 2, 0.9, (0, 0, 0), 1, 16],
            [cuenta,   (378,  490), 2, 0.9, (0, 0, 0), 1, 16],
            [fecha,     (118, 600), 2, 0.9, (0, 0, 0), 1, 16],
            [hora,      (350, 600), 2, 0.9, (0, 0, 0), 1, 16],
            [monto,     (118, 490), 2, 1.0, (0, 0, 0), 2, 16],
            [alias,     (220, 380), 2, 1.0, (0, 0, 0), 2, 16],

        ]
        if self._status == 'exito':
            field_ = [
                [trans.claveRastreo,  (118, 800), 2, 0.9, (0, 0, 0), 1, 16],
            ]
            for field in field_:
                fields.append(field)

        for field in fields:
            cv2.putText(img, *field)
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

        img_name = "comprobanteInguz.jpg"
        cv2.imwrite(img_name, img)
        comp_img = open(img_name, "rb")
        os.remove(img_name)
        return comp_img

    def cobro(self):
        trans_ = self.trans_
        trans = self._trans
        nombre = trans_.usuario_solicitante.Uprofile.get_nombre_completo()
        alias = f"@{trans_.usuario_solicitante.Uprofile.alias}"
        status = self._status
        avatar = trans_.usuario_solicitante.Uprofile.avatar
        monto = str(round(float(trans.monto), 2))
        fecha = trans.fechaValor.strftime("%m/%d/%Y")
        hora = trans.fechaValor.strftime("%H:%M:%S")
        concepto = trans.concepto

        if settings.SITE == "local":
            avatar = os.path.abspath(os.path.join(
                MEDIA_ROOT, avatar.avatar_img.name))
            avatar = cv2.imread(avatar, -1)
            img = cv2.imread(self._dir)
        elif settings.SITE not in "local":
            avatar = avatar.avatar_img.name
            avatar = imutils.url_to_image(avatar, -1)
            img = imutils.url_to_image(self._dir)
        fields = [
            [nombre,    (210, 350), 2, 0.9, (0, 0, 0), 1, 16],
            [concepto,  (118, 700), 2, 0.9, (0, 0, 0), 1, 16],
            [status,    (360, 490), 2, 0.9, (0, 0, 0), 1, 16],
            [trans.claveRastreo,  (118, 800), 2, 0.9, (0, 0, 0), 1, 16],
            [fecha,     (118, 600), 2, 0.9, (0, 0, 0), 1, 16],
            [hora,      (350, 600), 2, 0.9, (0, 0, 0), 1, 16],
            [monto,     (118, 490), 2, 1.0, (0, 0, 0), 2, 16],
            [alias,     (220, 380), 2, 1.0, (0, 0, 0), 2, 16],
        ]

        for field in fields:
            cv2.putText(img, *field)
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
        img_name = "comprobanteInguz.jpg"
        cv2.imwrite(img_name, img)
        comp_img = open(img_name, "rb")
        os.remove(img_name)
        return comp_img

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
        if self._status == 'exito':
            field_ = [
                [rastreo,  (112, 800), 2, 0.9, (0, 0, 0), 1, 16],
                [referencia, (112, 900), 2, 0.9, (0, 0, 0), 1, 16],
            ]
            for field in field_:
                fields.append(field)

        if settings.SITE == "local":
            img = cv2.imread(self._dir)
        elif settings.SITE not in "local":
            img = imutils.url_to_image(self._dir)
        for field in fields:
            cv2.putText(img, *field)
        otrosbancos = imutils.url_to_image(
            "https://phototest420.s3.amazonaws.com/{}".format(
                    "docs/stpstatics/OTROS_BANCOS.png"
            ),
            -1)
        otrosbancos = cv2.resize(otrosbancos, (250, 250))
        x_offset = 180
        y_offset = 0
        y1, y2 = y_offset, y_offset + otrosbancos.shape[0]
        x1, x2 = x_offset, x_offset + otrosbancos.shape[1]
        alpha_s = otrosbancos[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s
        for c in range(0, 3):
            img[y1:y2, x1:x2, c] = (alpha_s * otrosbancos[:, :, c] +
                                    alpha_l * img[y1:y2, x1:x2, c])
        img_name = "comprobanteSTP.jpg"
        cv2.imwrite(img_name, img)
        comp_img = open(img_name, "rb")
        os.remove(img_name)
        return comp_img

    def trans(self):
        if self._tipo.codigo == "18":
            print("entra?")
            return self.inguz()
        if self._tipo.codigo == "20":
            return self.cobro()
        if self._tipo.codigo == "2":
            return self.stp()