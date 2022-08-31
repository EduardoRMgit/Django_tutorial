from django.db import models
from django.contrib.auth.models import User


class Contacto(models.Model):
    OK = 'O'
    PEP = 'P'
    LISTANEGRA = 'N'

    STATUS_CHOICES = (
        (OK, ("Ok")),
        (PEP, "Politicamente Expuesto"),
        (LISTANEGRA, "Lista Negra")
    )

    nombre = models.CharField(max_length=40)
    nombreCompleto = models.CharField(max_length=200, null=True, default='')
    ap_paterno = models.CharField(max_length=30, default='')
    ap_materno = models.CharField(max_length=30, default='')
    banco = models.CharField(max_length=69)
    clabe = models.CharField(max_length=18)
    activo = models.BooleanField(default=True)
    verificacion = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=OK
    )
    user = models.ForeignKey(
        User,
        related_name='Contactos_Usuario',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.nombre

    class Meta():
        verbose_name_plural = 'Lista de Contactos'


# TODO ARREGLAR ESTA CHINGADERA PARA QUE SI FUNCIONE
'''@receiver(post_save, sender=Contacto)
def save_Contacto(sender, instance, **kwargs):
    data = {
        'id_entidad': 5500,
        'mothers_last_name': instance.ap_materno,
        'last_name': instance.ap_paterno,
        'name': instance.nombre,
    }
    resp = listaNegra(data)

    instance.verificacion = resp[1]

    if instance.verificacion == 'O':
        instance.nombreCompleto = instance.nombre + ' ' + \
            instance.ap_paterno + ' ' + \
            instance.ap_materno
    else:
        results = resp[0].get('results')[-1]
        nombre = results.get('nombre')
        apaterno = results.get('apaterno')
        amaterno = results.get('amaterno')
        instance.nombreCompleto = nombre + ' ' + apaterno + ' ' + amaterno

    post_save.disconnect(receiver=save_Contacto, sender=sender)
    instance.save()
    post_save.connect(receiver=save_Contacto, sender=sender)'''
