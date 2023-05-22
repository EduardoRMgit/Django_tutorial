from django.contrib import admin
from django.contrib.auth.models import User
from demograficos.models import (UserProfile,
                                 Cliente,
                                 Telefono,
                                 ComportamientoDiario,
                                 ComportamientoMensual,
                                 Contacto,
                                 RespuestaSeguridad,
                                 PreguntaSeguridad,
                                 Fecha,
                                 Direccion,
                                 TipoDireccion,
                                 EntidadFed,
                                 DocAdjunto,
                                 UserBeneficiario,
                                 UserDevice,
                                 Avatar,
                                 PerfilTransaccionalDeclarado,
                                 PasswordHistory,
                                 AliasInvalido,
                                 Proveedor)
from banca.models import Transaccion
from pld.models import (Customer)
from .cambio_password import PasswordResetUserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from cactus.settings import SITE
from import_export.admin import ExportActionMixin
from spei.deletecuentaSTP import delete_stp
from demograficos.utils.deletecustomer import pld_customer_delete


import logging


db_logger = logging.getLogger('db')


class RequiredForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(
        label="NIP",
        help_text=_(
            "El nip en bruto no se salva. Solo su hash, el cual se compara"
            " para verificar. Para cambiar el NIP se debe usar la app"
        ),
    )


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    form = RequiredForm
    exclude = ('password',)
    if SITE == "prod":
        readonly_fields = ['saldo_cuenta', ]


class RespuestaInline(admin.StackedInline):
    model = RespuestaSeguridad
    can_delete = False
    verbose_name_plural = 'Preguntas Seguridad'
    fk_name = 'user'


class FechaInline(admin.StackedInline):
    model = Fecha
    can_delete = False
    verbose_name_plural = 'Fechas'
    fk_name = 'user'


class UserTelefonoInline(admin.TabularInline):
    model = Telefono
    can_delete = False
    verbose_name_plural = 'Telefono'
    fk_name = 'user'
    exclude = ('fechaCreacion',)


class UserComportamientoDiarioInline(admin.TabularInline):
    model = ComportamientoDiario
    can_delete = False
    verbose_name_plural = 'Comportamiento diario'
    fk_name = 'user'


class UserComportamientoMensualInline(admin.TabularInline):
    model = ComportamientoMensual
    can_delete = False
    verbose_name_plural = 'Comportamiento mensual'
    fk_name = 'user'


class UserPLDCustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = 'Customer (UBCUBO)'
    fk_name = 'user'


class UserTransaccionInline(admin.TabularInline):
    model = Transaccion
    can_delete = False
    verbose_name_plural = 'Transacciones'
    fk_name = 'user'


class UserContactoInline(admin.TabularInline):
    model = Contacto
    can_delete = False
    verbose_name_plural = 'Lista de Contactos'
    fk_name = 'user'


class DireccionInLine(admin.TabularInline):
    model = Direccion
    can_delete = False
    verbose_name_plural = "Direcciones de Perfil"
    fk_name = "user"
    exclude = ('fechaCreacion',)


class DocAdjuntoInLine(admin.TabularInline):
    model = DocAdjunto
    can_delete = False
    verbose_name_plural = "Documentos de Perfil"
    fk_name = "user"


class BeneficiarioInLine(admin.TabularInline):
    model = UserBeneficiario
    can_delete = True
    verbose_name_plural = "Beneficiarios"
    fk_name = "user"
    extra = 0


class PerfilTransaccionalInLine(admin.TabularInline):
    model = PerfilTransaccionalDeclarado
    can_delete = True
    verbose_name_plural = "Perfil Transaccional Declarado"
    fk_name = "user"
    extra = 0


class ProveddorInLine(admin.TabularInline):
    model = Proveedor
    can_delete = True
    verbose_name_plural = "Proveedor"
    fk_name = "user"
    extra = 0


class UserProfileAdmin(ExportActionMixin, PasswordResetUserAdmin):
    inlines = (
        DireccionInLine,
        ProfileInline,
        FechaInline,
        RespuestaInline,
        UserTelefonoInline,
        UserPLDCustomerInline,
        UserTransaccionInline,
        UserComportamientoDiarioInline,
        UserComportamientoMensualInline,
        UserContactoInline,
        DocAdjuntoInLine,
        BeneficiarioInLine,
        PerfilTransaccionalInLine,
        ProveddorInLine
    )
    actions = ['registra_cuenta', 'delete_stp_cuenta', 'delete_pld_customer']

    list_filter = (
        'Uprofile__nivel_cuenta',
        'Uprofile__enrolamiento',
        'Uprofile__status',
        'is_active'
    )

    search_fields = (
        'username',
        'Uprofile__cuentaClabe',
        'Uprofile__curp',
        'Uprofile__alias'
    )

    list_display = ('username',
                    'get_alias',
                    'get_nombre',
                    'get_nivel',
                    'get_saldo',
                    'get_estado',
                    'get_curp',
                    'get_cuenta_clabe',
                    'get_enrolamiento',
                    'is_active'
                    )

    list_per_page = 25

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['first_name', 'last_name', 'username', 'email']

        return []

    def get_nombre(self, obj):
        return obj.Uprofile.get_nombre_completo()
    get_nombre.short_description = 'Nombre'

    def get_alias(self, obj):
        return obj.Uprofile.alias
    get_alias.short_description = 'Alias'

    def get_enrolamiento(self, obj):
        return obj.Uprofile.enrolamiento
    get_enrolamiento.short_description = 'Completo'
    get_enrolamiento.boolean = True

    def get_nivel(self, obj):
        return obj.Uprofile.nivel_cuenta
    get_nivel.short_description = 'Nivel'

    def get_saldo(self, obj):
        return ("$" + str(obj.Uprofile.saldo_cuenta))
    get_saldo.short_description = 'Saldo'

    def get_cuenta_clabe(self, obj):
        return obj.Uprofile.cuentaClabe
    get_cuenta_clabe.short_description = 'CLABE'

    def get_estado(self, obj):
        return obj.Uprofile.status
    get_estado.short_description = 'Estado'

    def get_curp(self, obj):
        return obj.Uprofile.curp
    get_curp.short_description = 'CURP'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserProfileAdmin, self).get_inline_instances(request, obj)

    def registra_cuenta(self, request, usuarios):

        for u in usuarios:
            try:
                u.Uprofile.registra_cuenta(u.first_name, u.last_name)
            except Exception as ex:
                print(ex)

    def delete_stp_cuenta(self, request, usuarios):
        for user in usuarios:
            try:
                id_, descripcion = delete_stp(user)
                if id_ == 0:
                    user.is_active = False
                    user.save()
                    msg_logg = "[STP delete cuenta] {}.".format(
                        user.Uprofile.cuentaClabe)
                    db_logger.info(msg_logg)
                elif id_:
                    msg = f"[ERROR STP delete cuenta] \
                        descripcion: {descripcion}"
                    db_logger.error(msg)
            except Exception as ex:
                msg = f"[ERROR accion STP delete cuenta] \
                        descripcion: {ex}"
                db_logger.error(msg)
        # if usuarios.count() != 1:
        #     print("Elegir sólo un usuario")
        #     return
        # u = usuarios.first()
        # print("Usuario: ", u)
        # up = u.Uprofile

        # curp = up.curp
        # up.curp = "AARA881202HDFLDL07"

        # first_name = u.first_name
        # u.first_name = "Aldo"

        # last_name = u.last_name
        # u.last_name = "Curiel"

        # ap_materno = up.apMaterno
        # up.apMaterno = "Moreno"

        # fecha_naciemiento = up.fecha_nacimiento
        # up.fecha_naciemiento = "19900101"
        # up.save()
        # u.save()

        # print(up.registra_cuenta())
        # up.curp = curp
        # u.first_name = first_name
        # u.last_name = last_name
        # up.apMaterno = ap_materno
        # up.fecha_nacimiento = fecha_naciemiento
        # up.save()
        # u.save()

    def delete_pld_customer(self, request, users):

        for user in users:
            try:
                pld_customer_delete(user.Uprofile.curp)
            except Exception as ex:
                msg = f"[ERROR action ubcubo delete customer] " \
                      f"descripcion: {ex}"
                db_logger.error(msg)


class ClienteAdmin(UserProfileAdmin):
    fieldsets = (
        (None, {'fields': ('username',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
    )
    inlines = (
        DireccionInLine,
        ProfileInline,
        FechaInline,
        RespuestaInline,
        UserTelefonoInline,
        UserPLDCustomerInline,
        UserTransaccionInline,
        UserComportamientoDiarioInline,
        UserComportamientoMensualInline,
        UserContactoInline,
        DocAdjuntoInLine,
        BeneficiarioInLine,
    )


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(PreguntaSeguridad)
# admin.site.unregister(Group)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(TipoDireccion)
admin.site.register(EntidadFed)
admin.site.register(UserDevice)
admin.site.register(Avatar)
# admin.site.register(Administradore, AdministradoreAdmin)
admin.site.register(PasswordHistory)
admin.site.register(AliasInvalido)
