import logging

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from banca.models import Transaccion, ErroresTransaccion, SaldoReservado
from demograficos.models import Contacto

from .stpTools import pago as stpPago, registra_cuenta_persona_fisica


db_logger = logging.getLogger("db")


class StpNotificacionEstadoDeCuenta(models.Model):
    cuenta = models.CharField(max_length=18, null=False, blank=True)
    empresa = models.CharField(max_length=15, null=False, blank=True)
    estado = models.CharField(max_length=1, null=False, blank=True)
    observaciones = models.CharField(max_length=512, null=False, blank=True)

    def __str__(self):
        return self.cuenta + " " + self.estado


class CuentaPersonaFisica(models.Model):
    """
    Modelo que representa el registro de una cuenta para una persona física.

    ``Attributes:``

    - nombre = models.CharField(max_length=164, null=True, blank=True)
    - apellido_paterno = models.CharField(max_length=64, null=True, blank=True)
    - apellido_materno = models.CharField(max_length=64, null=True, blank=True)
    - cuenta = models.CharField(max_length=20, null=True, blank=True)
    - empresa = models.CharField(max_length=100, null=True, blank=True)
    - rfc_curp = models.CharField(max_length=20, null=True, blank=True)
    - genero = models.CharField(max_length=1, null=True, blank=True)
    - fecha_nacimiento = models.CharField(max_length=8, null=True, blank=True)
    - entidad_fededativa = models.CharField(
          max_length=64, null=True, blank=True)
    - actividad_economica = models.CharField(
          max_length=64, null=True, blank=True)
    - calle = models.CharField(max_length=64, null=True, blank=True)
    - num_exterior = models.CharField(max_length=8, null=True, blank=True)
    - num_interior = models.CharField(max_length=8, null=True, blank=True)
    - colonia = models.CharField(max_length=64, null=True, blank=True)
    - alcaldia_municipio = models.CharField(
          max_length=, null=True, blank=True)
    - codigo_postal = models.CharField(max_length=100, null=True, blank=True)
    - pais_nacimiento = models.CharField(max_length=100, null=True, blank=True)
    - id_identificacion = models.CharField(max_length=100, null=True, blank=
    - telefono = models.CharField(max_length=100, null=True, blank=True)
    """

    nombre = models.CharField(max_length=164, null=True, blank=True)
    apellido_paterno = models.CharField(max_length=64, null=True, blank=True)
    apellido_materno = models.CharField(max_length=64, null=True, blank=True)
    cuenta = models.CharField(max_length=20, null=True, blank=True)
    empresa = models.CharField(max_length=100, null=True, blank=True)
    rfc_curp = models.CharField(max_length=20, null=True, blank=True)
    genero = models.CharField(max_length=1, null=True, blank=True)
    fecha_nacimiento = models.CharField(max_length=64, null=True, blank=True)
    entidad_fededativa = models.CharField(
        max_length=64, null=True, blank=True)
    actividad_economica = models.CharField(
        max_length=64, null=True, blank=True)
    calle = models.CharField(max_length=64, null=True, blank=True)
    num_exterior = models.CharField(max_length=64, null=True, blank=True)
    num_interior = models.CharField(max_length=64, null=True, blank=True)
    colonia = models.CharField(max_length=64, null=True, blank=True)
    alcaldia_municipio = models.CharField(
        max_length=64, null=True, blank=True)
    codigo_postal = models.CharField(max_length=5, null=True, blank=True)
    pais_nacimiento = models.CharField(max_length=32, null=True, blank=True)
    id_identificacion = models.CharField(max_length=32, null=True, blank=True)
    telefono = models.CharField(max_length=16, null=True, blank=True)
    folio_stp = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cuenta_clabe',
        blank=True,
        null=True
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def registra(self):
        '''
        Registra los datos haciendo uso del WS de STP.
        '''
        if self.fecha_nacimiento is not None:
            fecha_nac = self.fecha_nacimiento.strftime("%Y%m%d")
        else:
            fecha_nac = "19900101"

        print("EN spei cuenta: nombre:", self.nombre)
        print("EN spei last_name:", self.apellido_paterno)

        msg = f"[curp (3) registra() - modelsSPEI] ->{self.rfc_curp}<-"
        db_logger.info(msg)
        data_registro = {

            # Con Mayúsculas, sin acentos ni tildes ni coma ni punto ni guión
            'nombre': self.nombre.upper(),
            'apellidoPaterno': self.apellido_paterno.upper(),
            'apellidoMaterno': self.apellido_materno.upper(),

            #
            'cuenta': self.cuenta,
            'empresa': self.empresa,
            'rfcCurp': self.rfc_curp,

            # M = Mujer, H = Hombre
            # 'genero': "ND",  # self.genero,

            # AAAAMMDD

            'fechaNacimiento': fecha_nac,

            # De catálogo
            # 'entidadFededativa': "ND",  # self.entidad_fededativa,

            # De catálogo
            # 'actividadEconomica': "ND",  # self.actividad_economica,

            # Con Mayúsculas, sin acentos ni tildes ni coma ni punto ni guión
            # 'calle': "ND",  # self.calle.upper(),
            # 'numExterior': "ND",  # self.num_exterior.upper(),
            # 'numInterior': "ND",  # self.num_interior.upper(),
            # 'colonia': "ND",  # self.colonia.upper(),
            # 'alcaldiaMunicipio': "ND",  # self.alcaldia_municipio.upper(),
            # 'codigoPostal': "ND",  # self.codigo_postal.upper(),

            # De catálogo
            'paisNacimiento': self.pais_nacimiento,

            # INE
            # 'idIdentificacion': "ND",  # self.id_identificacion,

            #
            # 'telefono': self.telefono
        }

        # TODO: verificar la bandera de adminUtils registrocuenta
        return registra_cuenta_persona_fisica(data_registro)


class adminUtils(models.Model):
    """adminUtils se utiliza para habilitar o deshabilitar features

    ``Attributes:``

    -util: Es el nombre de la funcion o del toggle que se quiere usar, en
    este caso el campo util es para el toggle de "utilidades" en el admin.

    -activo: es un campo tipo Bool que funciona para prender y apagar el
    util. Esto resulta en una caja que puedes checar desde el admin para
    prender y apagar la funcion.
    """

    util = models.CharField('Utilidades', max_length=30)
    activo = models.BooleanField(default=False)

    class Meta():
        verbose_name_plural = 'Administrar Utilidades'

    def __str__(self):
        return self.util


class StpInstitution(models.Model):
    """Modelo que representa todas las instituciones soportadas por STP

    ``Attributes:``

    - name =CharField(max_length=50)
    - short_id =CharField(max_length=3)
    - long_id =CharField(max_length=5)
    """
    name = models.CharField(max_length=50)
    short_id = models.CharField(max_length=3)
    long_id = models.CharField(max_length=5)


class InstitutionBanjico(models.Model):
    """Modelo que representa todas las instituciones soportadas por BANJICO

    ``Attributes:``
    - name =CharField(max_length=150, null=True, blank=True)

    - short_name =CharField(max_length=50, null=True, blank=True)

    - short_id =CharField(max_length=3, null=True, blank=True)

    - long_id =CharField(max_length=5, null=True, blank=True)

    """
    name = models.CharField(max_length=150, null=True, blank=True)
    short_name = models.CharField(max_length=50, null=True, blank=True)
    short_id = models.CharField(max_length=3, null=True, blank=True)
    long_id = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.short_name


class StpTransaction(models.Model):
    """Modelo que representa una Transaccion
    ``Attributes:``
        - statusTrans = IntegerField(choices=POSSIBLE_STATES_VAINILLA,
                                        default=0)
        - institucionOrdenante = CharField(max_length=50,
                                                null=True,
                                                blank=True)
        - institucionBeneficiaria = CharField(max_length=50,
                                                null=True,
                                                blank=True)
        - institucionOrdenanteInt = many to one to through
                InstitutionBanjico models

        - institucionBeneficiariaInt = many to one to
                    the InstitutionBanjico models

        - transaccion = OneToOneField(Transaccion,
                                        on_delete=models.CASCADE,
                                        blank=True,
                                        null=True)
        - user =many to one  to the user models
        - stpId =CharField(max_length=50, null=True, blank=True)
        - stpMsg =CharField(max_length=200, null=True, blank=True)

        - nombre =CharField(max_length=100, null=True, blank=True)
        - banco =CharField(max_length=50, null=True, blank=True)
        - clabe =CharField(max_length=18, null=True)
        - concepto =CharField(max_length=128, null=True, blank=True)
        - referencia =CharField(max_length=18, null=True)
        - estado =CharField(max_length=32, null=True, blank=True)
        - empresa =CharField(max_length=64, null=True, blank=True)
        - folioOrigen =CharField(max_length=64, null=True, blank=True)
        - causaDevolucion =CharField(max_length=64, null=True, blank=True)
        - monto =CharField(max_length=64, null=True)
        - fechaOperacion =DateTimeField(default=timezone.now,
                                            null=True, blank=True)
        - claveRastreo =CharField(max_length=64, null=True)
        - nombreOrdenante = models.CharField(max_length=64,
                                             null=True, blank=True)
        - tipoCuentaOrdenante =CharField(max_length=64, null=True,
                                            blank=True)
        - cuentaOrdenante =CharField(max_length=64, null=True, blank=True)
        - rfcCurpOrdenante =CharField(max_length=64, null=True, blank=True)
        - nombreBeneficiario =CharField(max_length=64, null=True, blank=True)
        - tipoCuentaBeneficiario =CharField(max_length=64, null=True,
                                                blank=True)
        - cuentaBeneficiario =CharField(max_length=64, null=True,
                                            blank=True)
        - rfcCurpBeneficiario =CharField(max_length=64, null=True,
                                            blank=True)
        - conceptoPago =CharField(max_length=64, null=True, blank=True)
        - referenciaNumerica =CharField(max_length=64, null=True, blank=True)
        - time =DateTimeField(default=timezone.now)
        - ubicacion =CharField(max_length=64, null=True,
                                    blank=True)
        - balance =CharField(max_length=10, null=True, blank=True)
        - contacto =ForeignKey(
            Contacto,
            on_delete=models.CASCADE,
            related_name='contacto_stp_transaccion',
            blank=True,
            null=True
    """

    POSSIBLE_STATES = (
        (0, 'esperando respuesta'),
        (1, 'exito'),
        (2, 'devolucion')
    )
    stpEstado = models.IntegerField(choices=POSSIBLE_STATES, default=0)

    POSSIBLE_STATES_VAINILLA = (
        (0, 'STP'),
        (1, 'sendAbono'),
        (2, 'BanoError'),
        (3, 'InstitucionError'),
        (4, 'sendabonoEmpresaNoPermitida'),
        (5, 'sendabonoDesahabilitado'),
        (6, 'sendabonoErrorCuentaEmpresa')
    )

    rechazada = models.BooleanField(default=False)
    rechazadaMsj = models.CharField(max_length=200, null=True, blank=True)

    statusTrans = models.IntegerField(choices=POSSIBLE_STATES_VAINILLA,
                                      default=0)
    institucionOrdenante = models.CharField(max_length=50,
                                            null=True,
                                            blank=True)
    institucionBeneficiaria = models.CharField(max_length=50,
                                               null=True,
                                               blank=True)
    institucionOrdenanteInt = models.ForeignKey(InstitutionBanjico,
                                                on_delete=models.SET_NULL,
                                                blank=True,
                                                null=True,
                                                related_name='iO_iB')
    institucionBeneficiariaInt = models.ForeignKey(InstitutionBanjico,
                                                   on_delete=models.SET_NULL,
                                                   blank=True,
                                                   null=True,
                                                   related_name='iB_iB')
    transaccion = models.OneToOneField(Transaccion,
                                       on_delete=models.CASCADE,
                                       blank=True,
                                       null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_stp_transaccion',
        blank=True,
        null=True
    )
    stpId = models.CharField(max_length=50, null=True, blank=True)
    stpMsg = models.CharField(max_length=200, null=True, blank=True)

    nombre = models.CharField(max_length=100, null=True, blank=True)
    banco = models.CharField(max_length=50, null=True, blank=True)
    clabe = models.CharField(max_length=18, null=True)
    concepto = models.CharField(max_length=128, null=True, blank=True)
    referencia = models.CharField(max_length=18, null=True)
    estado = models.CharField(max_length=32, null=True, blank=True)
    empresa = models.CharField(max_length=64, null=True, blank=True)
    folioOrigen = models.CharField(max_length=64, null=True, blank=True)
    causaDevolucion = models.CharField(max_length=64, null=True, blank=True)
    monto = models.CharField(max_length=64, null=True)
    # fechaOperacion = # models.DateTimeField(default=timezone.now)
    fechaOperacion = models.CharField(max_length=64, null=True, blank=True)
    claveRastreo = models.CharField(max_length=64, null=True)
    nombreOrdenante = models.CharField(max_length=64, null=True, blank=True)
    tipoCuentaOrdenante = models.CharField(max_length=64, null=True,
                                           blank=True)
    cuentaOrdenante = models.CharField(max_length=64, null=True, blank=True)
    rfcCurpOrdenante = models.CharField(max_length=64, null=True, blank=True)
    nombreBeneficiario = models.CharField(max_length=64, null=True, blank=True)
    tipoCuentaBeneficiario = models.CharField(max_length=64, null=True,
                                              blank=True)
    cuentaBeneficiario = models.CharField(max_length=64, null=True,
                                          blank=True)
    rfcCurpBeneficiario = models.CharField(max_length=64, null=True,
                                           blank=True)
    conceptoPago = models.CharField(max_length=64, null=True, blank=True)
    referenciaNumerica = models.CharField(max_length=64, null=True, blank=True)
    time = models.DateTimeField(default=timezone.now)
    ubicacion = models.CharField(max_length=64, null=True,
                                 blank=True)
    balance = models.CharField(max_length=10, null=True, blank=True)
    contacto = models.ForeignKey(
        Contacto,
        on_delete=models.CASCADE,
        related_name='contacto_stp_transaccion',
        blank=True,
        null=True
    )
    tsLiquidacion = models.CharField(max_length=64, null=True, blank=True)
    folioCodi = models.CharField(max_length=64, null=True, blank=True)
    tipoPago = models.IntegerField(blank=True, null=True)
    saldoReservado = models.OneToOneField(
        SaldoReservado,
        null=True,
        blank=True,
        verbose_name="Saldo reservado",
        related_name="stpReservado",
        on_delete=models.CASCADE
    )
    reservado = models.CharField(max_length=64, null=True, default="0")
    OK = 'O'
    PEP = 'P'
    LISTANEGRA = 'N'

    STATUS_CHOICES = (
        (OK, ("Ok")),
        (PEP, "Politicamente Expuesto"),
        (LISTANEGRA, "Lista Negra")
    )
    verifListaNegra = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=OK
    )
    conciliado = models.BooleanField(default=False)
    url_cep = models.URLField(max_length=2056, blank=True, null=True)

    def __str__(self) -> str:
        txt = "Id Inguz: {} | StpId: {}"
        return txt.format(self.pk, self.stpId)

    def pago(self):
        data_pago = {}
        data_pago['clave_rastreo'] = self.claveRastreo
        data_pago['concepto'] = self.concepto
        data_pago['clabe'] = self.clabe
        data_pago['monto'] = self.monto
        data_pago['nombre_beneficiario'] = self.nombreBeneficiario
        data_pago['nombre_ordenante'] = self.user.get_full_name()
        data_pago['referencia'] = self.referenciaNumerica
        data_pago['cuenta_ordenante'] = self.cuentaOrdenante
        data_pago['empresa'] = self.empresa
        data_pago['folio_origen'] = self.folioOrigen
        data_pago['rfc_curp_beneficiario'] = (
            self.rfcCurpBeneficiario if self.rfcCurpBeneficiario else 'ND')
        data_pago['rfc_curp_ordenante'] = (
            self.rfcCurpOrdenante if self.rfcCurpOrdenante else 'ND')
        data_pago['tipo_cuenta_beneficiario'] = (
            self.tipoCuentaBeneficiario if self.tipoCuentaBeneficiario
            else '40')
        data_pago['tipo_cuenta_ordenante'] = (
            self.tipoCuentaOrdenante if self.tipoCuentaOrdenante else '40')
        data_pago['cuenta_beneficiario'] = self.cuentaBeneficiario
        data_pago['concepto_pago'] = self.conceptoPago
        data_pago['inst_contraparte'] = "846"

        # site = os.getenv("SITE", "local")
        # if site == "test":
        short_id = data_pago['cuenta_beneficiario'][:3]
        try:
            data_pago['inst_contraparte'] = InstitutionBanjico.objects.get(
                short_id=short_id).long_id
        except Exception as ex:
            print("ERROR al obtener inst contraparte: ", ex)

        resp = stpPago(data_pago)
        self.stpId = resp[0]  # TODO revisar los distintos tipos de error
        self.stpMsg = resp[1]

        if resp[0] <= 0:
            err = ErroresTransaccion.objects.get(codigo=-11)
            self.transaccion.errorRes = err
            self.transaccion.save()
            self.save()
        else:
            err = ErroresTransaccion.objects.get(codigo=0)
            self.transaccion.errorRes = err
            self.transaccion.save()
            self.save()
        return resp[0]


class FolioStp(models.Model):

    folio = models.IntegerField(default=100)

    def __str__(self):
        return f"Folio {self.folio}"

    def fol_dispatch(self):
        disp = self.folio
        self.folio += 1
        self.save()

        return disp


class ConciliacionSTP(models.Model):
    class Meta:
        verbose_name = "Conciliación STP por fecha"
        verbose_name_plural = "Conciliación STP por fechas"

    E = 'E'
    R = 'R'

    TIPO_ORDEN = (
        (E, ("Enviadas")),
        (R, ("Recibidas"))
    )

    fecha_inicio = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha inicial")
    fecha_fin = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha final")
    tipo_orden_conciliacion = models.CharField(
        max_length=1,
        choices=TIPO_ORDEN,
        default=E,
        verbose_name="Tipo de transacción"
    )
    conciliado = models.BooleanField(
        default=False,
        verbose_name="Conciliación realizada"
    )
    hora_de_conciliacion = models.DateTimeField(
        default=None,
        verbose_name="Fecha de la conciliación",
        null=True,
        blank=True
    )

    def __str__(self):
        txt = "Tipo {} del {} al {} "
        return txt.format(
            self.tipo_orden_conciliacion,
            self.fecha_inicio,
            self.fecha_fin)


class MovimientoConciliacion(models.Model):

    class Meta:
        verbose_name = "Movimiento Conciliado"
        verbose_name_plural = "Movimientos Conciliados"

    # estado = models.CharField(max_length=64, null=True, blank=True)
    # mensaje = models.CharField(max_length=64, null=True, blank=True)
    idEF = models.CharField(max_length=64, null=True, blank=True)
    claveRastreo = models.CharField(max_length=64, null=True)
    conceptoPago = models.CharField(max_length=64, null=True, blank=True)
    cuentaBeneficiario = models.CharField(max_length=64, null=True,
                                          blank=True)
    cuentaOrdenante = models.CharField(max_length=64, null=True, blank=True)
    empresa = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    estado = models.CharField(max_length=32, null=True, blank=True)
    fechaOperacion = models.DateField(auto_now=False, auto_now_add=False)
    institucionContraparte = models.CharField(max_length=64,
                                              null=True,
                                              blank=True)
    institucionOperante = models.CharField(max_length=50, null=True,
                                           blank=True)
    medioEntrega = models.CharField(max_length=64, null=True, blank=True)
    monto = models.CharField(max_length=64, null=True)
    nombreBeneficiario = models.CharField(
        max_length=64,
        null=True,
        blank=True)
    nombreOrdenante = models.CharField(max_length=64, null=True, blank=True)
    nombreCep = models.CharField(max_length=100, null=True, blank=True)
    rfcCep = models.CharField(max_length=64, null=True, blank=True)
    sello = models.CharField(max_length=200, null=True, blank=True)
    rfcCurpBeneficiario = models.CharField(max_length=64, null=True,
                                           blank=True)
    referenciaNumerica = models.CharField(
        max_length=200,
        null=True,
        blank=True)
    rfcCurpOrdenante = models.CharField(max_length=64, null=True,
                                        blank=True)
    tipoCuentaBeneficiario = models.CharField(max_length=64, null=True,
                                              blank=True)
    tipoCuentaOrdenante = models.CharField(max_length=64, null=True,
                                           blank=True)
    tipoPago = models.IntegerField(blank=True, null=True)
    tsCaptura = models.CharField(max_length=64, null=True, blank=True)
    tsLiquidacion = models.CharField(max_length=64, null=True, blank=True)
    causaDevolucion = models.CharField(max_length=1024, null=True, blank=True)
    urlCEP = models.CharField(max_length=1024, null=True, blank=True)
    stpTransaction = models.OneToOneField(
        StpTransaction,
        verbose_name="Transacción STP conciliada",
        related_name="StpConciliada",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    conciliacion = models.ForeignKey(
        ConciliacionSTP,
        on_delete=models.CASCADE,
        related_name='ConciliacionSTP'
    )
    conciliada = models.BooleanField(default=False)

    def __str__(self):
        txt = "idEF: {} | {}"
        return txt.format(self.idEF, self.fechaOperacion)
