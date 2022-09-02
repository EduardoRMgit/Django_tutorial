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
                                 ComponentValidated,
                                 Direccion,
                                 TipoDireccion,
                                 EntidadFed,
                                 DocAdjunto,
                                 UserBeneficiario,
                                 UserDevice)
from banca.models import Transaccion
from pld.models import (Customer,
                        Contrato,
                        Movimiento)
from .cambio_password import PasswordResetUserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _


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
    exclude = ('blocked_date', 'password')


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


class UserPLDContratoInline(admin.StackedInline):
    model = Contrato
    can_delete = False
    verbose_name_plural = 'Contrato (UBCUBO)'
    fk_name = 'user'


class UserPLDMovimientoInline(admin.TabularInline):
    model = Movimiento
    can_delete = False
    verbose_name_plural = 'Movimiento (PLD)'
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


class ProfileComponentInline(admin.StackedInline):
    model = ComponentValidated
    can_delete = False
    verbose_name_plural = "Validaciones de Perfil"
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
    can_delete = False
    verbose_name_plural = "Beneficiarios"
    fk_name = "user"
    extra = 0


class UserProfileAdmin(PasswordResetUserAdmin):
    inlines = (
        DireccionInLine,
        ProfileInline,
        FechaInline,
        RespuestaInline,
        UserTelefonoInline,
        UserPLDCustomerInline,
        UserPLDContratoInline,
        UserPLDMovimientoInline,
        UserTransaccionInline,
        UserComportamientoDiarioInline,
        UserComportamientoMensualInline,
        UserContactoInline,
        ProfileComponentInline,
        DocAdjuntoInLine,
        BeneficiarioInLine
        )
    actions = ['registra_cuenta']
    list_filter = ('is_staff',
                   )

    list_display = ('Uprofile',
                    'get_saldo',
                    'get_estado',
                    'get_curp',
                    'get_rfc',
                    'get_cuenta_clabe',
                    )

    list_select_related = ('Uprofile', )

    list_per_page = 25

    def get_saldo(self, obj):
        return obj.Uprofile.saldo_cuenta
    get_saldo.short_description = 'Saldo cuenta'

    def get_cuenta_clabe(self, obj):
        return obj.Uprofile.cuentaClabe
    get_cuenta_clabe.short_description = 'Cuenta Clabe'

    def get_estado(self, obj):
        return obj.Uprofile.status
    get_estado.short_description = 'Estado'

    def get_curp(self, obj):
        return obj.Uprofile.curp
    get_curp.short_description = 'Check CURP'

    def get_rfc(self, obj):
        return obj.Uprofile.rfc
    get_rfc.short_description = 'Check RFC'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserProfileAdmin, self).get_inline_instances(request, obj)

    def get_queryset(self, request):
        qs = super(UserProfileAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(username=request.user.username)
        return qs

    def registra_cuenta(self, request, usuarios):

        for u in usuarios:
            try:
                u.Uprofile.registra_cuenta(u.first_name, u.last_name)
            except Exception as ex:
                print(ex)

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
        UserPLDContratoInline,
        UserPLDMovimientoInline,
        UserTransaccionInline,
        UserComportamientoDiarioInline,
        UserComportamientoMensualInline,
        UserContactoInline,
        ProfileComponentInline,
        DocAdjuntoInLine,
        BeneficiarioInLine
        )

# from demograficos.models import UserProfile, Telefono
# from banca.models import Transaccion
# from pld.models import (Customer,
#                         CustomerD,
#                         adminUtils,
#                         Contrato,
#                         ContratoD,
#                         Movimiento)
# from pld.utils.customer import llamada1
# from pld.utils.contract import llamada2
#
#
# def save_model(self, request, obj, form, change):
#     super().save_model(request, obj, form, change)
#     admin_Util = adminUtils.objects.get(id=1)
#     aprobado = False
#     stat = ""
#     cod = ""
#     bak = ""
#     if admin_Util.activo:
#         obj.tienePLD = True
#         obj.save()
#         tel = Telefono.objects.last()
#         lastD = CustomerD.objects.last()
#         last = Customer.objects.last()
#         data = {'id_entidad': lastD.id_entidad,
#                 'tipo': lastD.tipo,
#                 'nombre': obj.first_name,
#                 'actua_cuenta_propia': lastD.actua_cuenta_propia,
#                 'rfc': obj.Uprofile.rfc,
#                 'curp': obj.Uprofile.curp,
#                 'apaterno': obj.last_name,
#                 'amaterno': obj.Uprofile.apMaterno,
#                 'telefono_fijo': tel.telefono
#                 }
#         print('NEL, NO ES COCA... ES HARINA\n')cuentaClabe
#         [bak, cod, stat] = llamada1(data)
#         last.id_back = bak
#         last.status_code = stat
#         last.mensaje = cod
#         if stat == 200:
#             aprobado = True
#         Customer.objects.create(id_entidad=lastD.id_entidad,
#                                 tipo=lastD.tipo,
#                                 nombre=obj.first_name,
#                                 actua_cuenta_propia=(
#                                     lastD.actua_cuenta_propia),
#                                 rfc=obj.Uprofile.rfc,
#                                 curp=obj.Uprofile.curp,
#                                 apaterno=obj.last_name,
#                                 amaterno=obj.Uprofile.apMaterno,
#                                 telefono_fijo=tel.telefono,
#                                 status_code=stat,
#                                 mensaje=cod,
#                                 id_back=bak,
#                                 tienePLD=aprobado,
#                                 )
#         self.message_user(request, "PLD:{}".format(cod))
#         last.save()
#         rnd = bak
#         ultD = ContratoD.objects.last()
#         ult = Contrato.objects.last()
#         data = {'id_entidad': last.id_entidad,
#                 'rfc': obj.Uprofile.rfc,
#                 'curp': obj.Uprofile.curp,
#                 'no_credito': rnd,
#                 # 'no_credito': id.no_credito,
#                 'unidad_credito': ultD.unidad_credito,
#                 'tipo_moneda': ultD.tipo_moneda,
#                 'T1': ultD.T1,
#                 'T2': ultD.T2,
#                 'T3': ultD.T3,
#                 'instrumento_monetario':
#                     ultD.instrumento_monetario,
#                 'canales_distribucion': ultD.canales_distribucion,
#                 'Estado': ultD.Estado
#                 }
#         print(data, '\nPINCHE CUMBION BIEN LOCO')
#         [cod, stat] = llamada2(data)
#         ult.status_code = stat
#         ult.mensaje = cod
#         Contrato.objects.create(id_entidad=ultD.id_entidad,
#                                 rfc=obj.Uprofile.rfc,
#                                 curp=obj.Uprofile.curp,
#                                 no_credito=rnd,
#                                 unidad_credito=ultD.unidad_credito,
#                                 tipo_moneda=ultD.tipo_moneda,
#                                 T1=ultD.T1,
#                                 T2=ultD.T2,
#                                 T3=ultD.T3,
#                                 instrumento_monetario=(
#                                     ultD.instrumento_monetario),
#                                 canales_distribucion=(
#                                     ultD.canales_distribucion),
#                                 Estado=ultD.Estado,
#                                 status_code=stat,
#                                 mensaje=cod,
#                                 )
#         self.message_user(request, "PLD:{}".format(cod))
#         ult.save()


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(PreguntaSeguridad)
# admin.site.unregister(Group)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(TipoDireccion)
admin.site.register(EntidadFed)
admin.site.register(UserDevice)
# admin.site.register(Administradore, AdministradoreAdmin)
