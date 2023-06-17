from arcus.utils.conciliacionpagos import conciliacion_arcus_pagos
from arcus.utils.uploadarcus import upload_arcus
from cactus.settings import (ARCUS_HOST,
                             ARCUS_USER,
                             ARCUS_PASS)
import paramiko
import os


def sftp_connect():

    doc, contenido = conciliacion_arcus_pagos()

    path = os.path.join('', doc.name)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ARCUS_HOST,
                   port='22',
                   username=ARCUS_USER,
                   password=ARCUS_PASS)
    sftp = client.open_sftp()
    sftp.chdir('IN')
    archivo_conciliacion = sftp.file(path, 'w')
    archivo_conciliacion.write(contenido)
    archivo_conciliacion.close()
    sftp.close()
    client.close()
    upload_arcus(path, contenido)
    os.remove(path)
