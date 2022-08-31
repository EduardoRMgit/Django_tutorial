from django.db import models


"""aditional information for adminUtils.
``Attributes:``
    adminUtils se utiliza para controlar algunas features que se pueden
    prender y apagar con un toggle, por ejemplo, la funcion de notificacion
    de Slack (que solo funciona cuando esta toggle-on)

    -util: Es el nombre de la funcion o del toggle que se quiere usar, en
    este caso el campo util es para el toggle de "utilidades" en el admin.

    -activo: es un campo tipo Bool que funciona para prender y apagar el
    util. Esto resulta en una caja que puedes checar desde el admin para
    prender y apagar la funcion.
"""


class adminUtils(models.Model):
    util = models.CharField('Utilidades', max_length=30)
    activo = models.BooleanField(default=False)

    class Meta():
        verbose_name_plural = 'Administrar Utilidades'

    def __str__(self):
        return self.util
