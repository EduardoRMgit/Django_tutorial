import os
import cv2
from banca.models import Comprobante
from spei.models import StpTransaction
from django.conf import settings
import imutils
from banca.utils.url_preassigned import get_file_preassigned
import time
from datetime import timedelta

if settings.SITE == "local":
    from cactus.settings import MEDIA_ROOT
elif settings.SITE == "prod":
    region = "us-east-2"
elif settings.SITE not in "prod":
    region = "us-east-1"
content = "image/jpeg"
time_stamp = time.time()


class CompTrans(object):
    def __init__(self, trans):
        try:
            self.trans_ = trans
            trans = trans.transaccion.transaccion
        except Exception:
            pass
        self._trans = trans
        self._tipo = self._trans.tipoTrans
        self._codigo = self._tipo.codigo
        self._status = self._trans.statusTrans.nombre
        if self._status == "exito":
            codigo = self._codigo
        if self._status == "rechazada":
            codigo = int(self._codigo)
            codigo += 1
            codigo = str(codigo)
        self._tp = Comprobante.objects.get(codigo=codigo).template
        if settings.SITE == "local":
            self._dir = os.path.abspath(
                os.path.join(MEDIA_ROOT, self._tp.name))
            self._tp = cv2.imread(self._dir)
        elif settings.SITE not in "local":
            self._urlc = "/docs/docs/plantillas/"
            self._dir = self._tp.url

    def inguz(self, show=False):
        trans = self._trans
        inguz_trans = InguzTransaction.objects.get(transaccion=trans)
        alias = f"@{trans.user.Uprofile.alias}"
        avatar = trans.user.Uprofile.avatar
        monto = "${:.2f}".format(round(float(trans.monto), 2))
        cuenta = f"*{inguz_trans.contacto.clabe[14:]}"
        fechaValor = trans.fechaValor - timedelta(hours=6)
        fecha = fechaValor.strftime("%d/%m/%Y")
        hora = fechaValor.strftime("%H:%M:%S")
        concepto = trans.concepto

        if settings.SITE == "local":
            avatar = os.path.abspath(os.path.join(
                MEDIA_ROOT, avatar.avatar_img.name))
            avatar = cv2.imread(avatar, -1)
            img = cv2.imread(self._dir)
        elif settings.SITE not in "local":
            avatar = avatar.avatar_img.url
            avatar = imutils.url_to_image(avatar, -1)
            img = imutils.url_to_image(self._dir)

        fields = [
            [concepto,  (118, 700), 2, 0.9, (0, 0, 0), 1, 16],
            [cuenta,   (378,  490), 2, 0.9, (0, 0, 0), 1, 16],
            [fecha,     (118, 600), 2, 0.9, (0, 0, 0), 1, 16],
            [hora,      (350, 600), 2, 0.9, (0, 0, 0), 1, 16],
            [monto,     (118, 490), 2, 1.0, (0, 0, 0), 2, 16],
            [alias,     (190, 340), 2, 0.8, (0, 0, 0), 1, 16],

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

        img_name = f"{time_stamp}comprobanteInguz.jpg"
        cv2.imwrite(img_name, img)
        comp_img = open(img_name, "rb")
        os.remove(img_name)
        path_file = 'docs/' + img_name
        url = get_file_preassigned(comp_img, path_file, region, content)
        return url

    def cobro(self):
        trans_ = self.trans_
        trans = self._trans
        alias = f"@{trans_.usuario_solicitante.Uprofile.alias}"
        status = self._status
        avatar = trans_.usuario_solicitante.Uprofile.avatar
        monto = "${:.2f}".format(round(float(trans.monto), 2))
        fechaValor = trans.fechaValor - timedelta(hours=6)
        fecha = fechaValor.strftime("%d/%m/%Y")
        hora = fechaValor.strftime("%H:%M:%S")
        concepto = trans.concepto

        if settings.SITE == "local":
            avatar = os.path.abspath(os.path.join(
                MEDIA_ROOT, avatar.avatar_img.name))
            avatar = cv2.imread(avatar, -1)
            img = cv2.imread(self._dir)
        elif settings.SITE not in "local":
            avatar = avatar.avatar_img.url
            avatar = imutils.url_to_image(avatar, -1)
            img = imutils.url_to_image(self._dir)
        fields = [
            [concepto,  (118, 700), 2, 0.9, (0, 0, 0), 1, 16],
            [status,    (360, 490), 2, 0.9, (0, 0, 0), 1, 16],
            [trans.claveRastreo,  (118, 800), 2, 0.9, (0, 0, 0), 1, 16],
            [fecha,     (118, 600), 2, 0.9, (0, 0, 0), 1, 16],
            [hora,      (350, 600), 2, 0.9, (0, 0, 0), 1, 16],
            [monto,     (118, 490), 2, 1.0, (0, 0, 0), 1, 16],
            [alias,     (158, 340), 2, 0.8, (0, 0, 0), 1, 16],
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
        img_name = f"{time_stamp}comprobanteInguz.jpg"
        cv2.imwrite(img_name, img)
        comp_img = open(img_name, "rb")
        os.remove(img_name)
        path_file = 'docs/' + img_name
        url = get_file_preassigned(comp_img, path_file, region, content)
        return url

    def stp(self):
        trans = self._trans
        stp_trans = StpTransaction.objects.get(
            transaccion=trans)
        importe = "${:,.2f}".format(round(float(trans.monto), 2))
        fechaValor = trans.fechaValor - timedelta(hours=6)
        fecha = fechaValor.strftime("%d/%m/%Y")
        hora = fechaValor.strftime("%H:%M:%S")
        concepto = trans.concepto
        cuenta = f"*{stp_trans.cuentaBeneficiario[14:]}"
        rastreo = trans.claveRastreo
        referencia = StpTransaction.objects.get(
            transaccion=trans).referenciaNumerica

        fields = [
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
            otrosbancos = os.path.abspath(
                os.path.join(MEDIA_ROOT, "OTROS_BANCOS.png"))
            otrosbancos = cv2.imread(otrosbancos)
        elif settings.SITE not in "local":
            url = settings.AWS_STATIC_PHOTOTEST
            otrosbancos = imutils.url_to_image(
                "https://{}/docs/stpstatics/OTROS_BANCOS.png".format(url), -1)
            img = imutils.url_to_image(self._dir)
        for field in fields:
            cv2.putText(img, *field)

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
        img_name = f"{time_stamp}comprobanteSTP.jpg"
        cv2.imwrite(img_name, img)
        comp_img = open(img_name, "rb")
        os.remove(img_name)
        path_file = 'docs/' + img_name
        url = get_file_preassigned(comp_img, path_file, region, content)
        return url

    def trans(self):
        if self._tipo.codigo == "18":
            print("entra?")
            return self.inguz()
        if self._tipo.codigo == "20":
            return self.cobro()
        if self._tipo.codigo == "2":
            return self.stp()
