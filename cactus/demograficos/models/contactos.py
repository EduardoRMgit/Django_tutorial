from django.db import models
from django.contrib.auth.models import User
from demograficos.models import UserProfile
from django.dispatch import receiver
from django.db.models.signals import pre_save


class Contacto(models.Model):

    class Meta():
        verbose_name_plural = 'Lista de Contactos'

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
    alias_inguz = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    avatar_url = models.URLField(
        max_length=600,
        null=True,
        blank=True
    )
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
    frecuencia = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.nombre


@receiver(pre_save, sender=Contacto)
def get_inguz(sender, instance, **kwargs):
    if instance.clabe[:10] == "6461802180":
        try:
            contacto = UserProfile.objects.get(
                cuentaClabe=instance.clabe, status="O").user
            instance.alias_inguz = contacto.Uprofile.alias
            instance.avatar_url = contacto.Uprofile.avatar.avatar_img.url
            print(instance.avatar_url)
        except Exception:
            instance.alias_inguz = "Cuenta inguz no encontrada"


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
