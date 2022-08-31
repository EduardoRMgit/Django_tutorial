from django.db import models
# from django.utils import timezone
from django.contrib.auth.models import User


class Fecha(models.Model):
    """

    ``Attributes:``

    - user(forgein):many to one User models

    - creacion (DateTime):Fecha de Creacion blank=True, null=True

    - bloqueo(DateTime):Fecha de bloqueo blank=True, null=True
    - ultimo_acceso(DateTime):Fecha de ultimo acceso blank=True, null=True
    - cancelacion(DateTime):Fecha de Cancelacion blank=True, null=True
    - reactivacion(DateTime):Fecha de Reactivacion blank=True, null=True
    - cambio_de_nip(DateTime):Fecha de cambio de nip blank=True, null=True)
    - cambio_de_contraseña(DateTimeField):Fecha de cambio de contraseña
      blank=True, null=True
    - cambio_de_dispositivo(DateTime):Fecha de cambio de cambio_de_dispositivo
      blank=True, null=True)
    - cambio_id_cliente_telefonico(DateTime):Fecha de cambio id telefono
      blank=True, null=True
    - registro_codi(DateTime):Fecha de cambio registro codi blank=True,
      null=True
    - creacion_dde(DateTimeField):creacion dde blank=True, null=True
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='Ufecha')

    creacion = models.DateTimeField(blank=True, null=True)
    bloqueo = models.DateTimeField(blank=True, null=True)
    ultimo_acceso = models.DateTimeField(blank=True, null=True)
    cancelacion = models.DateTimeField(blank=True, null=True)
    reactivacion = models.DateTimeField(blank=True, null=True)
    cambio_de_nip = models.DateTimeField(blank=True, null=True)
    cambio_de_contraseña = models.DateTimeField(blank=True, null=True)
    cambio_de_dispositivo = models.DateTimeField(blank=True, null=True)
    cambio_id_cliente_telefonico = models.DateTimeField(blank=True, null=True)
    registro_codi = models.DateTimeField(blank=True, null=True)
    creacion_dde = models.DateTimeField(blank=True, null=True)

    @classmethod
    def populate(cls):
        for user in User.objects.all():
            try:
                fecha = user.Ufecha.set_created()
            except Exception as e:
                print(e)
                fecha = Fecha.objects.create(user=user)
                fecha.set_created()
                fecha.save()

    def set_created(self):
        self.creacion = self.user.date_joined
        self.ultimo_acceso = self.user.last_login
        self.bloqueo = self.user.Uprofile.blocked_date
        self.save()

    # def update(self):
    #     self.bloqueo = self.user.Uprofile.blocked_date
    #     self.ultacceso = self.user.last_login
    #     self.save()
