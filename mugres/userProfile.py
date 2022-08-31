# -*- coding: utf-8 -*-
from django.db import models
from django_countries.fields import CountryField
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .productos import Productos
from django.core.files.storage import FileSystemStorage


# Catalogo de Solicitud registro
class StatusRegistro(models.Model):
    status = models.CharField(max_length=30)

    def __str__(self):
        return self.status


# Catalogo de Solicitud registro
class StatusCuenta(models.Model):
    status = models.CharField(max_length=30)

    def __str__(self):
        return self.status


# Indice disponible que tiene el usuario
class IndiceDisponible(models.Model):

    porcentaje = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.porcentaje)


class UserProfile(models.Model):
    """aditional information for the user.

    ``Attributes:``

        - pk(int): Primary Key, one to one field to the django standard user \
            model

        - country: The country the user is from, ForeignKey(Country)

        - blocked_reason(char): Which is why the account was blocked

        - blocked_date(datetime): Date the account was locked

        - login_attempts(int): Number of login attempts

        - login_attempts(int): Number of login attemts to be blocked.

        - login_attempts_inside(int): Number of attemts inside to be blocked.

        - status(char): Status of the UserProfile
    """

    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='Uprofile')
    OK = 'O'
    BLOCKED = 'B'
    CANCELED = 'C'
    STATUS_CHOICES = (
        (OK, ("Ok")),
        (BLOCKED, "Bloqueada"),
        (CANCELED, u"Suscripción cancelada")
    )
    BLOCKED = 'B'
    TOO_MANY_LOGIN_ATTEMPTS = 'T'
    TOO_MANY_LOGIN_ATTEMPTS_INSIDE = 'I'
    NOT_BLOCKED = 'K'
    BLOCKED_REASONS = (
        (BLOCKED, ("Su cuenta ha sido bloqueada, "
                   "por favor contactenos")),
        (TOO_MANY_LOGIN_ATTEMPTS, ("Su cuenta ha sido bloqueada "
                                   "por exceso de intentos de "
                                   u"inicio de sesión")),
        (TOO_MANY_LOGIN_ATTEMPTS_INSIDE, ("Su cuenta ha sido bloqueada "
                                          "por exceso de intentos de "
                                          u"inicio de sesión")),
        (NOT_BLOCKED, "OK")
    )

    blocked_reason = models.CharField(
        max_length=1,
        choices=BLOCKED_REASONS,
        default=NOT_BLOCKED
    )
    blocked_date = models.DateTimeField(null=True,blank=True)
    login_attempts = models.PositiveSmallIntegerField(default=0)
    login_attempts_inside = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=OK
    )
    apMaterno = models.CharField(max_length=30,blank=True)
    sexo = models.CharField(
        max_length = 1,
        blank=True
    )
    curp = models.CharField(max_length=20,blank=True)
    rfc = models.CharField(max_length=20,blank=True)
    verificacion_curp = models.BooleanField(default=False)
    fechaNaciemiento = models.DateField(null=True,blank=True)
    verificacion_email = models.BooleanField(default=False)
    statusRegistro = models.ForeignKey(
            StatusRegistro,
            on_delete=models.SET_NULL,
            blank=True,
            null=True,
            related_name='status_registro'
    )
    statusCuenta = models.ForeignKey(
            StatusCuenta,
            on_delete=models.SET_NULL,
            blank=True,
            null=True,
            related_name='status_cuenta'
    )
    autorizado = models.BooleanField(default=False)
    country = CountryField()
    ine = models.ImageField(upload_to='docs/ine', blank=True, null=True)
    ineValidado = models.BooleanField(default=False)
    ineReverso = models.ImageField(upload_to='docs/ineReverso', blank=True, null=True)
    ineReversoValidado = models.BooleanField(default=False)
    compobantedom = models.ImageField(upload_to='docs/comprobante', blank=True, null=True)
    compobantedomValidado = models.BooleanField(default=False)

    indiceDisponible = models.ForeignKey(
            IndiceDisponible,
            on_delete=models.SET_NULL,
            blank=True,
            null=True,
    )

    class Meta():
        verbose_name_plural = 'Perfil del usuario'

    def __str__(self):
        return str(self.user.username)

    def reset_login_attempts(self):
        """
        **Description**
            This function set parameter of Account lockout to default values
        **Parameters**
            self
        """
        self.blocked_reason = self.NOT_BLOCKED
        self.blocked_date = None
        self.login_attempts = 0
        self.login_attempts_inside = 0
        self.save()

    def is_blocked_by_attempts(self):
        """
        **Description**
            This function unlocks user or keep blocked
        **Parameters**
            self
        **Returns**
            blocked: if login_attempts if greater than or equal to 5
        """
        blocked = self.login_attempts >= 5
        if blocked:

            # Check if 30 minutes have passed since blocked
            if (timezone.now() -
                    self.blocked_date) > constants.LOGIN_ATTEMPTS_BLOCKED_TIME:
                # Then unlock
                self.reset_login_attempts()
                return False

            # Else, block
            self.blocked_reason = self.TOO_MANY_LOGIN_ATTEMPTS
            self.blocked_date = timezone.now()
            self.save()
        return blocked

    def add_login_attempt(self):
        """
        **Description**
            This function adds an attempt to login_attempts field and \
            returns number of login attempts. Block if necessary
        **Parameters**
            self
        **Returns**
            self.login_attempts: number of login attempts
        """
        self.login_attempts += 1

        # Block if necessary
        if self.login_attempts >= 5:
            self.blocked_reason = self.TOO_MANY_LOGIN_ATTEMPTS
            self.blocked_date = timezone.now()
        self.save()
        return self.login_attempts

    def add_login_attempt_inside(self):
        """
        **Description**
            This function adds an attempt to login_attempts inside field and
            returns number of login attempts. Block if necessary
        **Parameters**
            self
        **Returns**
            self.login_attempts_inside: number of login attempts inside the
            system
        """
        self.login_attempts_inside += 1

        # Block if necessary
        if self.login_attempts_inside >= 5:
            self.blocked_reason = self.TOO_MANY_LOGIN_ATTEMPTS_INSIDE
        self.save()
        return self.login_attempts_inside

    def is_blocked_by_attempts_inside(self):
        """
        **Description**
            This function unlocks user or keep blocked
        **Parameters**
            self
        **Returns**
            blocked: if login_attempts if greater than or equal to 5
        """
        blocked = self.login_attempts_inside >= 5
        if blocked:
            self.blocked_reason = self.BLOCKED
            self.blocked_date = None
            self.save()
            return True
        return blocked


@receiver(post_save, sender=User)
def create_user_UserProfile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_UserProfile(sender, instance, **kwargs):
    instance.Uprofile.save()


# Cada vez que sucede algo, Un log..Historia de cambio de curp etc, domicilios etc.
class UserNotas(models.Model):
    nota = models.CharField(max_length=500)
    fechaCreacion = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        User,
        related_name='User_notas',
        on_delete=models.CASCADE,
    )
    logger = models.ForeignKey(
        User,
        related_name='WhoDidIt',
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return self.nota


# Historia de las lineas de credito que ha tenido el Usuario
class HistoriaLinea(models.Model):
    user = models.ForeignKey(
        User,
        related_name='User_HistoriaLinea',
        on_delete=models.CASCADE,
    )
    lineaCredito = models.FloatField(null=True, blank=True)
    lineaDisponible = models.FloatField(null=True, blank=True)
    fechaApertura = models.DateTimeField(null=True, blank=True)
    fechaCierre = models.DateTimeField(null=True, blank=True)
    fechaCongelada = models.DateTimeField(null=True, blank=True)
    fechaUltTrans = models.DateTimeField(null=True, blank=True)
    saldoCuenta = models.FloatField(null=True, blank=True)
    fechaLinea = models.DateTimeField(default=timezone.now)
    productos = models.ForeignKey(
        Productos,
        on_delete=models.CASCADE,
        related_name='User_HistoriaLinea'

    )
