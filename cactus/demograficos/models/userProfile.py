# -*- coding: utf-8 -*-
import logging

from django.db import models
from random import randint
from django_countries.fields import CountryField
from django.utils import timezone
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from banca.models.productos import Productos
from banca.models.entidades import CodigoConfianza
from banca.models import NivelCuenta
from demograficos.models import Direccion


from spei.clabe import CuentaClabe


from django.contrib.auth.base_user import AbstractBaseUser


db_logger = logging.getLogger('db')


class PreguntaSeguridad(models.Model):
    """Specifies telefono's kind .

    ``Attributes:``

        - tipo (char): Especifica preguntas de seguridad.
           - Especifica el tipo de NIP.
           - Establece una pregunta de Pregunta de seguridad.
           - Establece una respuesta secreta unica.
    """
    tipo_nip = models.BooleanField(default=False)
    pregunta = models.CharField(max_length=60, blank=True)
    respuesta_secreta = models.ManyToManyField(
        User,
        through='RespuestaSeguridad',
        through_fields=('pregunta', 'user')
    )

    def __str__(self):
        return self.pregunta

    class Meta():
        verbose_name_plural = 'Preguntas de seguridad'


# Catalogo de Solicitud registro
class StatusRegistro(models.Model):
    """aditional information for the user.
    ``Attributes:``
        - status(char): can be:
            - TELEFONO REGISTRADO Y VALIDADO
            - INE Y COMPROBANTE DE DOMICILIO REGISTRADOS
            - PERFIL DE USUARIO COMPLETADO
            - NIP Y PREGUNTA SECRETA REGISTRADOS
            - CONTRATO DE APERTURA ACEPTADO
            - PRIMER DEPOSITO REALIZADO
    """
    descripcion = models.CharField(max_length=100)
    codigo = models.CharField(max_length=4)

    def __str__(self):
        return self.descripcion


# Catalogo de Solicitud registro
class StatusCuenta(models.Model):
    """aditional information for the user.
    ``Attributes:``
        - status(char): can be:
            - ACTIVO
            - BLOQUEADA
            - PERFIL DE USUARIO COMPLETADO
            - NIP Y PREGUNTA SECRETA REGISTRADOS
            - CONTRATO DE APERTURA ACEPTADO
            - PRIMER DEPOSITO REALIZADO
    """
    status = models.CharField(max_length=60)

    def __str__(self):
        return self.status


# Indice disponible que tiene el usuario
class IndiceDisponible(models.Model):

    porcentaje = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.porcentaje)


def uProfilenuller(klass):
    klass._meta.get_field('password').null = True
    klass._meta.get_field('password').blank = True
    return klass


class Avatar(models.Model):

    opciones_genero = (
        ("M", "Mujer"),
        ("H", "Hombre"),
        ("O", "Otro")
    )
    genero = models.CharField(null=True,
                              blank=True,
                              max_length=15,
                              choices=opciones_genero)
    avatar_img = models.ImageField(upload_to='avatars',
                                   blank=True,
                                   null=True)
    name = models.CharField(max_length=128,
                            blank=True,
                            null=True)

    description = models.CharField(max_length=128,
                                   blank=True,
                                   null=True)

    activo = models.BooleanField(default=True)

    avatar_min = models.ImageField(
        upload_to='avatars',
        blank=True,
        verbose_name="Avatar miniatura",
        null=True)

    def __str__(self):
        return str(self.name)


@uProfilenuller
class UserProfile(AbstractBaseUser):
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
        - statusRegistro(foreign): many to one to the StatusRegistro Model. \
            This field will help on the screen that will be shown to the user.
        - statusCuenta(foreign): many to one to the StatusCuenta Model. \
            This will help if the user requests a blocked or other reasons \
            like fraud prevention.
        - ine(foreing): many to one to the DocAdjunto Model. DocAdjunto in \
            general will never be deleted. This field is for the front side \
            of the INE card.
        - ineReverso(foreing): many to one to the DocAdjunto Model. \
            DocAdjunto in general will never be deleted. This field \
            is for the back side of the INE card.
        - comprobantedom(foreing): many to one to the DocAdjunto Model. \
            DocAdjunto in general will never be deleted. This field is \
            for the front side of the proof of address.
        - nip(char): is the password specifically for transactions.
        - statusNip(char): any of UNSET, ACTIVE or BLOCKED. Used when user \
            sets the NIP or request a blocked of it.
        -aceptaKitLegal(datetime): used when user accepts the terms of use of \
            the app.
    """

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

    UN = 'U'
    AC = "A"
    BL = "B"

    NIP_CHOICES = (
        (UN, "UNSET"),
        (AC, "ACTIVE"),
        (BL, "BLOCKED")
    )

    USERNAME_FIELD = 'apMaterno'

    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='Uprofile'
    )

    nivel_cuenta = models.ForeignKey(
        NivelCuenta,
        default=1,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    alias = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )

    blocked_reason = models.CharField(
        max_length=1,
        choices=BLOCKED_REASONS,
        default=NOT_BLOCKED
    )

    blocked_date = models.DateTimeField(null=True, blank=True)
    login_attempts = models.PositiveSmallIntegerField(default=0)
    login_attempts_inside = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=OK
    )
    apMaterno = models.CharField(max_length=30, blank=True, null=True)
    sexo = models.CharField(
        max_length=1,
        blank=True,
        default=""
    )
    curp = models.CharField(max_length=20, blank=True, null=True)
    numero_INE = models.CharField(max_length=20, null=True, blank=True)
    verificacion_curp = models.BooleanField(default=False)
    fecha_nacimiento = models.DateField(null=True, blank=True)
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
    country = CountryField(blank=True, null=True)
    pais_origen_otro = models.CharField(max_length=50,
                                        blank=True,
                                        null=True,
                                        verbose_name='Pais de nacimiento')
    ineCaptura = models.ImageField(upload_to='docs/ine', blank=True, null=True)
    ineReversoCaptura = models.ImageField(upload_to='docs/ineReverso',
                                          blank=True,
                                          null=True)
    comprobanteDomCaptura = models.ImageField(upload_to='docs/comprobanteDom',
                                              blank=True,
                                              null=True)
    indiceDisponible = models.ForeignKey(
        IndiceDisponible,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    statusNip = models.CharField(
        max_length=1,
        choices=NIP_CHOICES,
        default=UN)
    nip = models.CharField(max_length=6, null=True, blank=True)
    aceptaKitLegal = models.DateTimeField(blank=True, null=True)
    kitComisiones = models.FileField(upload_to='docs/pdfLegal',
                                     blank=True, null=True)
    kitTerminos = models.FileField(upload_to='docs/pdfLegal',
                                   blank=True, null=True)
    kitPrivacidad = models.FileField(upload_to='docs/pdfLegal',
                                     blank=True, null=True)
    kitDeclaraciones = models.FileField(upload_to='docs/pdfLegal',
                                        blank=True, null=True)

    saldo_cuenta = models.FloatField(null=True, blank=True, default=0)
    cuentaClabe = models.CharField(max_length=18, blank=True)
    ocupacion = models.CharField(max_length=30, blank=True)
    nacionalidad = models.CharField(max_length=30, blank=True)
    ciudad_nacimiento = models.CharField(max_length=30, blank=True)
    rfc = models.CharField(max_length=20, null=True, blank=True)
    con_seguro = models.BooleanField(default=False)

    id_dde = models.IntegerField(null=True, blank=True)
    fechaCreacion_dde = models.DateTimeField(null=True, blank=True)
    confirmacion_dde = models.BooleanField(default=False)
    saldo_dde = models.FloatField(null=True, blank=True, default=0)

    validacion_telefono = models.BooleanField(default=False)
    validacion_perfil = models.BooleanField(default=False)
    validacion_direccion = models.BooleanField(default=False)
    validacion_cuenta_en_STP = models.BooleanField(default=False)

    usuarioCodigoConfianza = models.ForeignKey(
        CodigoConfianza,
        on_delete=models.DO_NOTHING,
        blank=True,
        related_name='userProfile_codigo_de_confianza',
        null=True)
    ocr_ok = models.BooleanField(default=False)
    cuenta_clabe_bloqueada = models.BooleanField(default=False)

    # campos codi
    registro_completo = models.BooleanField(default=False)
    predeterminada = models.BooleanField(default=False)
    keySource = models.CharField(max_length=255, null=True, blank=True)
    aliasSms = models.CharField(max_length=255, null=True,  blank=True)
    dvSub = models.CharField(max_length=255, null=True, blank=True)
    verificada = models.BooleanField(default=False)
    cd = models.CharField(max_length=255, null=True, blank=True)
    deOmision = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    avatar = models.ForeignKey(Avatar,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)
    avatar_url = models.URLField(
        max_length=600,
        null=True,
        blank=True
    )
    enrolamiento = models.BooleanField(default=False)

    class Meta():
        verbose_name_plural = 'Perfil del usuario'

    def __str__(self):
        return str(self.user.username)

    def get_nombre_completo(self):
        x = []
        if self.user.first_name:
            x.append(self.user.first_name)
        if self.user.last_name:
            x.append(self.user.last_name)
        if self.apMaterno:
            x.append(self.apMaterno)
        full_name = " ".join(x)
        return full_name

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
            # TODO define constants.LOGIN_ATTEMPTS_BLOCKED_TIME
            if (timezone.now() - self.blocked_date) > 30:

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

    def registra_cuenta(self, first_name, last_name):
        from spei.models import CuentaPersonaFisica, FolioStp

        try:
            folio_stp = FolioStp.objects.last()
            folio = folio_stp.fol_dispatch()
            cuenta_clabe = CuentaClabe(folio_stp.fol_dispatch())
            while UserProfile.objects.filter(
                    cuentaClabe=cuenta_clabe).count() > 0:
                folio = folio_stp.fol_dispatch()
                cuenta_clabe = CuentaClabe(folio_stp.fol_dispatch())

            cuenta = CuentaPersonaFisica.objects.create(
                nombre=first_name,
                apellido_paterno=last_name,
                apellido_materno=self.apMaterno,
                cuenta=cuenta_clabe,
                empresa="ZYGOO",
                rfc_curp=self.curp,
                fecha_nacimiento=self.fecha_nacimiento,
                pais_nacimiento="187",
                user=self.user,
                folio_stp=folio
            )
            registro_cuenta = cuenta.registra()
            cuenta.cuenta = cuenta_clabe
            cuenta.folio_stp = folio
            cuenta.save()
            self.cuentaClabe = cuenta_clabe
            self.save()

            db_logger.info("registro_cuenta STP({}): {}".format(
                cuenta_clabe,
                str(registro_cuenta)))
            id_alternativo = 0
            while registro_cuenta[0] == 3:
                id_alternativo += 1
                nuevo_folio = folio_stp.fol_dispatch()
                cuenta_clabe = CuentaClabe(nuevo_folio)
                cuenta.cuenta = cuenta_clabe
                cuenta.folio_stp = nuevo_folio
                cuenta.save()
                self.cuentaClabe = cuenta_clabe
                self.save()
                registro_cuenta = cuenta.registra()
                db_logger.info("registro_cuenta STP: " + str(registro_cuenta))
        except Exception as ex:
            db_logger.info("{} {} {} {} ---> {}".format(
                "Error resgistrando clabe ",
                cuenta_clabe,
                " para ",
                self.user,
                ex))


@receiver(post_save, sender=User)
def create_user_UserProfile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# First, define the Manager subclass.
class ClienteManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=False,
                                             is_staff=False)


class Cliente(User):
    objects = ClienteManager()

    class Meta:
        proxy = True


class INE_Info(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isFront = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    nombre = models.CharField(max_length=30, blank=True, null=True)
    a_paterno = models.CharField(max_length=30, blank=True, null=True,
                                 verbose_name="Apellido Paterno")
    a_materno = models.CharField(max_length=30, blank=True, null=True,
                                 verbose_name="Apellido Materno")

    calle = models.CharField(max_length=150, blank=True, null=True)
    colonia = models.CharField(max_length=50, blank=True, null=True)
    delegacion = models.CharField(max_length=50, blank=True, null=True)

    fecha = models.CharField(max_length=50, blank=True, null=True)

    clave_elector = models.CharField(max_length=19, blank=True, null=True)
    folio = models.CharField(max_length=30, blank=True, null=True)
    curp = models.CharField(max_length=30, blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    municipio = models.IntegerField(blank=True, null=True)
    localidad = models.IntegerField(blank=True, null=True)
    seccion = models.IntegerField(blank=True, null=True)
    edad = models.IntegerField(blank=True, null=True)
    sexo = models.CharField(max_length=7, blank=True, null=True)
    anio = models.IntegerField(blank=True, null=True)
    vigencia = models.IntegerField(blank=True, null=True)
    emision = models.IntegerField(blank=True, null=True)


class INE_Reg_Attempt(models.Model):
    user = models.ForeignKey(User, related_name='AttemptsSet',
                             on_delete=models.CASCADE)
    front = models.OneToOneField(INE_Info, null=True,
                                 on_delete=models.CASCADE,
                                 related_name='front_Attempt')
    back = models.OneToOneField(INE_Info, null=True, on_delete=models.CASCADE,
                                related_name='back_Attempt')
    attempts = models.PositiveSmallIntegerField(default=0, blank=True,
                                                null=True)
    approved = models.BooleanField(default=0, blank=True, null=True)

    def compare(self):
        # string distance farola recursiva
        self.attempts += 1

        def dist(s, len_s, t, len_t):
            if len_s == 0:
                return len_t
            if len_t == 0:
                return len_s
            if s[len_s-1] == t[len_t-1]:
                cost = 0
            else:
                cost = 1
            arg1 = dist(s, len_s - 1, t, len_t)+1
            arg2 = dist(s, len_s, t, len_t - 1)+1
            arg3 = dist(s, len_s-1, t, len_t-1)+cost

            return min(arg1, arg2, arg3)
        mistakes = 0
        chars = 0
        for attr, value in self.front.__dict__.items():
            if not isinstance(value, str):
                continue
            if "num" in attr:
                continue
            if "cur" in attr:
                continue
            valueInBack = eval('self.back.'+attr)
            d1 = len(valueInBack)
            d2 = len(value)
            chars += max(d1, d2)
            mistakes += dist(valueInBack, d1, value, d2)
        self.approved = mistakes/chars < 0.2


@receiver(post_save, sender=User)
def save_user_UserProfile(sender, instance, **kwargs):
    instance.Uprofile.save()


class RestorePassword(models.Model):
    passTemporal = models.CharField(max_length=6)
    activo = models.BooleanField(default=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def validate(self, testPassword):
        return self.passTemporal == testPassword


class RespuestaSeguridad(models.Model):
    respuesta_secreta = models.CharField(max_length=100, blank=True)
    tipo_nip = models.BooleanField(default=False)
    pregunta = models.ForeignKey(
        PreguntaSeguridad,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.respuesta_secreta


# Cada vez que sucede algo,
# Un log..Historia de cambio de curp etc, domicilios etc.
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


class Parentesco(models.Model):

    parentesco = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.parentesco


class UserBeneficiario(models.Model):
    user = models.ForeignKey(
        User,
        related_name='User_Beneficiario',
        on_delete=models.CASCADE,
    )
    direccion = models.ForeignKey(
        Direccion,
        related_name='Beneficiario_direccion',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    sexo = models.CharField(max_length=1, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    nombre = models.CharField(max_length=30, blank=True)
    parentesco = models.CharField(max_length=30, blank=True)
    apellido_materno = models.CharField(max_length=30, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=30, blank=True, null=True)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    correo_electronico = models.EmailField(max_length=100,
                                           blank=True, null=True)
    rfc = models.CharField(max_length=30, blank=True, null=True)
    curp = models.CharField(max_length=30, blank=True, null=True)
    parentesco = models.ForeignKey(
        Parentesco,
        on_delete=models.SET_NULL,
        related_name='Parentesco_Beneficiario',
        null=True,
        blank=True
    )
    participacion = models.FloatField(null=True, blank=True)
    activo = models.BooleanField(default=True, null=True)
    direccion_L1 = models.CharField(max_length=200, blank=True, null=True)
    direccion_L2 = models.CharField(max_length=200, blank=True, null=True)
    dir_num_int = models.CharField(max_length=20, blank=True, null=True)
    dir_num_ext = models.CharField(max_length=20, blank=True, null=True)
    dir_colonia = models.CharField(max_length=80, blank=True, null=True)
    dir_CP = models.CharField(max_length=6, blank=True, null=True)
    dir_estado = models.CharField(max_length=30, blank=True, null=True)
    dir_municipio = models.CharField(max_length=90, blank=True, null=True)
    verif_curp = models.BooleanField(default=False, blank=True, null=True)
    # Estas lineas son para verificar la construccion de un curp
    # Comparar: si hay match - continuar, de lo contrario - levantar flag
    # Esto se puede incluir en el resolve de los queries de user y Uprofile

    def __str__(self):
        return self.nombre


class UserDevice(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_device',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    os = models.CharField(max_length=100, blank=True, null=True)
    mac = models.CharField(max_length=100, blank=True, null=True)
    gps = models.CharField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)
    unique_id = models.CharField(max_length=100, blank=True, null=True,
                                 unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    dev_model = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.unique_id)


class NipTemporal(models.Model):

    user = models.ForeignKey(
        User,
        related_name='user_nipTemp',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    fecha = models.DateTimeField(default=timezone.now)
    nip_temp = models.CharField(max_length=6, blank=True, null=True)
    attempts = models.PositiveSmallIntegerField(default=0, blank=True,
                                                null=True)
    activo = models.BooleanField(default=True)

    def save(self, check=None, *args, **kwargs):
        if check is None:
            self.nip_temp = randint(1000, 9999)
            super().save(*args, **kwargs)

    def __str__(self):
        return str(self.fecha)
