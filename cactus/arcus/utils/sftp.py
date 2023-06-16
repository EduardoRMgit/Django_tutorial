from arcus.utils.conciliacionpagos import conciliacion_arcus_pagos
from arcus.utils.uploadarcus import upload_arcus
from cactus.settings import (ARCUS_HOST,
                             ARCUS_USER,
                             ARCUS_PASS)
import pysftp
import os


def sftp_connect():

    doc, contenido = conciliacion_arcus_pagos()

    path = os.path.join('', doc.name)
    with pysftp.Connection(ARCUS_HOST,
                           username=ARCUS_USER,
                           password=ARCUS_PASS) as sftp:
        with sftp.cd('IN'):
            sftp.put(path)
    upload_arcus(path, contenido)
    os.remove(path)
