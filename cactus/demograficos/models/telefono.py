from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils import timezone
from demograficos.utils.sms import send_sms
import random
import datetime


class TipoTelefono(models.Model):
    """
    ``Attributes:``
        - tipo (Char): Max 30 chars. 1:Movil | 2:Casa | 3:Oficina
    """

    tipo = models.CharField(max_length=30)

    def __str__(self):
        return self.tipo


class ProveedorTelefonico(models.Model):
    """Specifies telefono's kind .

    ``Attributes:``

        - proveedor (char): Specifies telephone's service provider.

        - country (countryfield): Phone service provider's country.
    """
    proveedor = models.CharField(max_length=30)
    country = CountryField(default="MX")

    class Meta:
        verbose_name_plural = 'Proveedores telefonicos'

    def __str__(self):
        return self.proveedor


class Telefono(models.Model):
    """User's phone.

    ``Attributes:``

        - telefono (char): user's telephone.

        - extension (countryfield): telefono's extension.

        - fechaCreacion (datetime): Date created.

        - country (countryfield): telephone's country.

        - codigos (char): ????.

        - activo (boolean): ???

        - validado (boolean): Validated status. True after authentication.

        - user (foreign): many to one to the django standard user model.

        - proveedorTelefonico (foreign): many to one to the Proveedor
            Telefonico model.

        - tipoTelefono (foreign): many to one to the TipoTelefono model.
    """

    telefono = models.CharField(max_length=12, blank=True, null=True)
    extension = models.CharField(max_length=6, blank=True, null=True)
    fechaCreacion = models.DateTimeField(default=timezone.now)
    country = CountryField(blank=True, null=True)
    prefijo = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=False)
    validado = models.BooleanField(default=False)

    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='user_telefono'
    )

    proveedorTelefonico = models.ForeignKey(
        ProveedorTelefonico,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    tipoTelefono = models.ForeignKey(
        TipoTelefono,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def send_token(self, test=False):
        pin = random.randint(100000, 999999)
        if test:
            ssid = []
        else:
            ssid = send_sms(self.country.name,
                            self.telefono, str(pin))
        PhoneVerification.objects.create(telefono=self,
                                         ssid=ssid,
                                         token=pin)

    def is_valid(self, token):
        tokenActual = self.PVTelefono.last()

        delta = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc) - \
            tokenActual.fechaCreacion < \
            datetime.timedelta(hours=2)
        if str(token) == tokenActual.token and delta:
            self.validado = True
            self.activo = True
            self.save()
            return True
        else:
            return False

    def __str__(self):
        return str(self.telefono)


class PhoneVerification(models.Model):
    """
    ``Attributes:``
        - token (Char): verifica token de telefono max_length=10, blank=True
        - ssid  (char): id unico asignado max_length=40, blank=True
        - fechaCreacion (datetime): fecha creada
        - telefono (foregin): many to one to Telefono model
    """
    token = models.CharField(max_length=10, blank=True)
    ssid = models.CharField(max_length=40, blank=True)
    fechaCreacion = models.DateTimeField(default=timezone.now)

    telefono = models.ForeignKey(
        Telefono,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='PVTelefono'
    )

    def __str__(self):
        return self.token
