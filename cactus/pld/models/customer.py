from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Customer(models.Model):
    """

    ``Attributes:``

    - Descripcion:

    - id_entidad = IntegerField(default=0)
    - tipo = IntegerField(default=0)
    - actividad_empresarial = IntegerField(
      default=0, null=True, blank=True)
    - sector_economico = IntegerField(
        default=0, null=True, blank=True)
    - apaterno = CharField(max_length=60, default=0,
                                blank=True, null=True)
    - amaterno = CharField(max_length=60, default=0,
                                blank=True, null=True)
    - nombre = CharField(max_length=90, default=0, blank=True, null=True)
    - vinculado = IntegerField(
      default=0, null=True, blank=True)
    - actua_cuenta_propia = IntegerField(default=0)
    - genero = CharField(max_length=1, null=True, blank=True)
    - rfc = CharField(max_length=15, default=0, blank=True, null=True)
      #  LLave UNIQUE: CURP
    - curp = CharField(max_length=18, default=0, blank=True, null=True)
    - fecha_nacimiento = DateField(null=True, blank=True)
    - pais_nacimiento = CountryField(null=True, blank=True)
    - nacionalidad = CountryField(null=True, blank=True)
    - e_f_nacimiento = CharField(max_length=60, null=True, blank=True)
    - telefono_fijo = CharField(max_length=20, null=True, blank=True)
    - telefono_movil = CharField(max_length=30, null=True, blank=True)
    - correo_electronico = CharField(max_length=90, null=True, blank=True)
    - profesion = CharField(max_length=60, null=True, blank=True)
    - actividad = CharField(max_length=120, null=True, blank=True)
    - no_empleados = IntegerField(default=0, null=True, blank=True)
    - actividad_cnbv = IntegerField(default=0, null=True, blank=True)
    - origen_ingresos = CharField(max_length=60, null=True, blank=True)
    - or_pais = CountryField(null=True, blank=True)
    - or_localidad = CharField(max_length=60, null=True, blank=True)
    - dr_localidad = CharField(max_length=60, null=True, blank=True)
    - or_actividad = CharField(max_length=90, null=True, blank=True)
    - fines_credito = CharField(max_length=60, null=True, blank=True)
    - puesto_gobierno = CharField(max_length=60, blank=True, null=True)
    - descripcion_puesto = CharField(max_length=60, blank=True, null=True)
    - periodo_puesto = CharField(max_length=60, blank=True, null=True)
    - calle =.CharField(max_length=60, null=True, blank=True)
    - no_exterior = CharField(max_length=60, null=True, blank=True)
    - no_interior = CharField(max_length=10, null=True, blank=True)
    - cp = CharField(max_length=10, null=True, blank=True)
    - colonia = CharField(max_length=90, null=True, blank=True)
    - municipio = CharField(max_length=100, null=True, blank=True)
    - ciudad = CharField(max_length=60, null=True, blank=True)
    - ef_domicilio = CharField(max_length=60, null=True, blank=True)
    - estado_domicilio = CharField(max_length=60, null=True, blank=True)
    - pais_domicilio = CountryField(null=True, blank=True)
    - fecha_proxima_revision = DateField(null=True, blank=True)
    - comentarios = CharField(max_length=420, null=True, blank=True)
    - mensaje = CharField(max_length=420, null=True, blank=True)
    - id_back = CharField(max_length=69, blank=True, null=True)
    - no_cliente = CharField(max_length=60, blank=True, null=True)
    - created_at = DateField(null=True, blank=True)
    - updated_at = DateField(null=True, blank=True)
    - status_code = CharField(max_length=3, blank=True, null=True)
    - tienePLD = BooleanField(default=False)
      # id del expediente que se actualizo:
    - id_back = CharField(max_length=69, null=True, blank=True)
    - lista_negra = CharField(max_length=10000, null=True, blank=True)
    - user = many to one
    """
    id_entidad = models.IntegerField(default=0)
    tipo = models.IntegerField(default=0)
    actividad_empresarial = models.IntegerField(
        default=0, null=True, blank=True)
    sector_economico = models.IntegerField(
        default=0, null=True, blank=True)
    apaterno = models.CharField(max_length=60, default=0,
                                blank=True, null=True)
    amaterno = models.CharField(max_length=60, default=0,
                                blank=True, null=True)
    nombre = models.CharField(max_length=90, default=0, blank=True, null=True)
    vinculado = models.IntegerField(
        default=0, null=True, blank=True)
    actua_cuenta_propia = models.IntegerField(default=0)
    genero = models.CharField(max_length=1, null=True, blank=True)
    rfc = models.CharField(max_length=15, default=0, blank=True, null=True)
    #  LLave UNIQUE: CURP
    curp = models.CharField(max_length=18, default=0, blank=True, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    pais_nacimiento = models.CharField(max_length=30, blank=True, null=True)
    nacionalidad = models.CharField(max_length=30, blank=True, null=True)
    e_f_nacimiento = models.CharField(max_length=60, null=True, blank=True)
    telefono_fijo = models.CharField(max_length=20, null=True, blank=True)
    telefono_movil = models.CharField(max_length=30, null=True, blank=True)
    correo_electronico = models.CharField(max_length=90, null=True, blank=True)
    profesion = models.CharField(max_length=60, null=True, blank=True)
    actividad = models.CharField(max_length=120, null=True, blank=True)
    no_empleados = models.IntegerField(default=0, null=True, blank=True)
    actividad_cnbv = models.IntegerField(default=0, null=True, blank=True)
    origen_ingresos = models.CharField(max_length=60, null=True, blank=True)
    or_pais = CountryField(null=True, blank=True)
    or_localidad = models.CharField(max_length=60, null=True, blank=True)
    dr_localidad = models.CharField(max_length=60, null=True, blank=True)
    or_actividad = models.CharField(max_length=90, null=True, blank=True)
    fines_credito = models.CharField(max_length=60, null=True, blank=True)
    puesto_gobierno = models.CharField(max_length=60, blank=True, null=True)
    descripcion_puesto = models.CharField(max_length=60, blank=True, null=True)
    periodo_puesto = models.CharField(max_length=60, blank=True, null=True)
    calle = models.CharField(max_length=60, null=True, blank=True)
    no_exterior = models.CharField(max_length=60, null=True, blank=True)
    no_interior = models.CharField(max_length=10, null=True, blank=True)
    cp = models.CharField(max_length=10, null=True, blank=True)
    colonia = models.CharField(max_length=90, null=True, blank=True)
    municipio = models.CharField(max_length=100, null=True, blank=True)
    ciudad = models.CharField(max_length=60, null=True, blank=True)
    ef_domicilio = models.CharField(max_length=60, null=True, blank=True)
    estado_domicilio = models.CharField(max_length=60, null=True, blank=True)
    pais_domicilio = CountryField(null=True, blank=True)
    fecha_proxima_revision = models.DateField(null=True, blank=True)
    comentarios = models.CharField(max_length=420, null=True, blank=True)
    mensaje = models.CharField(max_length=2000, null=True, blank=True)
    no_cliente = models.CharField(max_length=60, blank=True, null=True)
    created_at = models.DateField(null=True, blank=True)
    updated_at = models.DateField(null=True, blank=True)
    status_code = models.CharField(max_length=3, blank=True, null=True)
    tienePLD = models.BooleanField(default=False)
    # id del expediente que se actualizo:
    id_back = models.CharField(max_length=69, null=True, blank=True)
    lista_negra = models.CharField(max_length=10000, null=True, blank=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='Ucustomer')
    riesgo = models.CharField(max_length=255, null=True, blank=True)
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.user)
