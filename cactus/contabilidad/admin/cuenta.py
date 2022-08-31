from django.contrib import admin
from django.utils.html import format_html

from contabilidad.models import (CuentaSaldo, ContableCuenta, CuentaTipo,
                                 ContableMovimiento, TipoContableCuenta)


class MovimientosContaAdmin(admin.ModelAdmin):
    model = ContableMovimiento


class CuentaSaldoAdmin(admin.ModelAdmin):
    list_display = ('nombre',
                    'clabe',
                    'saldo',)

    ordering = ['id']


def colored(background, color, field):
    return format_html('<div style="background:{}; color:{};"><b>{}</b></div>',
                       background,
                       color,
                       field)


def _format_field(field):
    return format_html('<div>{}</div>'.format(field))


def _format_field_cuenta(obj, field_name):
    field_value = obj.__dict__.get(field_name)
    if obj.cuenta_padre is None:
        return colored('orange', 'white', field_value)
    return _format_field(field_value)


def _show_field(es_cuenta_padre, value):
    if es_cuenta_padre:
        return colored('orange', 'white', value)
    return _format_field(value)


def balanza_get_queryset(id_tipo):
    return TipoContableCuenta.objects.get(
        id=id_tipo).cuentas.all()


class MovimientoAdminInLine(admin.TabularInline):
    model = ContableMovimiento
    can_delete = False
    can_edit = False
    verbose_name_plural = 'Movimientos'
    extra = 0
    ordering = ['fecha', ]
    fields = ['_saldo_inicial',
              '_cargo',
              '_abono',
              '_saldo_final',
              'fecha']
    readonly_fields = fields

    def _saldo_inicial(self, obj):
        return _format_field(obj.saldo_inicial)

    def _cargo(self, obj):
        return _format_field(obj.cargo)

    def _abono(self, obj):
        return _format_field(obj.abono)

    def _saldo_final(self, obj):
        return _format_field(obj.saldo_final)


class ContableCuentaAdmin(admin.ModelAdmin):
    list_display = ('_codigo',
                    '_nombre',
                    '_saldo_inicial',
                    '_cargo',
                    '_abono',
                    '_saldo',)

    ordering = ['codigo', ]
    inlines = (MovimientoAdminInLine, )
    actions = ['renombra_cuentas']

    def renombra_cuentas(self, request, cuentas):
        _cuentas = [['1102', '1-0-02-001-02-002'],
                    ['1102-0001', '1-0-02-001-04-002'],
                    ['1102-0002', '1-0-02-001-04-001'],
                    ['1107', '2-0-16-004-03-009'],
                    ['1107-0001', '2-0-16-004-04-001'],
                    ['2101', '2-0-16-006-03-016'],
                    ['2101-0001', '2-0-16-016-04-008'],
                    ['2102', '2-0-16-001-02-006'],
                    ['2102-0001', '2-0-16-006-03-019'],
                    ['2103', '2-0-02-000-01-001'],
                    ['2103-0001', '2-0-02-001-03-001'],
                    ['3100', '4-0-02-001-02-004'],
                    ['3100-0001', '4-0-02-004-03-001'],
                    ['5202', '6-0-04-002-02-015'],
                    ['5202-0001', '6-0-04-015-03-001'],
                    ['1102', '1-0-02-001-02-002'],
                    ['1102-0001', '1-0-02-001-04-002'],
                    ['1102-0002', '1-0-02-001-04-001'],
                    ['1107', '2-0-16-004-03-009'],
                    ['1107-0001', '2-0-16-004-04-001'],
                    ['2101', '2-0-16-006-03-016'],
                    ['2101-0001', '2-0-16-016-04-008'],
                    ['2102', '2-0-16-001-02-006'],
                    ['2102-0001', '2-0-16-006-03-019'],
                    ['2103', '2-0-02-000-01-001'],
                    ['2103-0001', '2-0-02-001-03-001'],
                    ['2104', '2-0-16-004-03-009'],
                    ['2104-0001', '2-0-16-004-04-003'],
                    ['3100', '4-0-02-001-02-004'],
                    ['3100-0001', '4-0-02-004-03-001'],
                    ['4101', '5-0-02-001-02-007'],
                    ['4101-0001', '5-0-02-007-03-001'],
                    ['5202', '6-0-04-002-02-015'],
                    ['5202-0001', '6-0-04-015-03-001'],
                    ['1102', '1-0-02-001-02-002'],
                    ['1102-0001', '1-0-02-001-04-002'],
                    ['1102-0002', '1-0-02-001-04-001'],
                    ['1107', '2-0-16-004-03-009'],
                    ['1107-0001', '2-0-16-004-04-001'],
                    ['2101', '2-0-16-006-03-016'],
                    ['2101-0001', '2-0-16-016-04-008'],
                    ['2103', '2-0-02-000-01-001'],
                    ['2103-0001', '2-0-02-001-03-001'],
                    ['2104', '2-0-16-004-03-009'],
                    ['2104-0001', '2-0-16-004-04-003'],
                    ['3100', '4-0-02-001-02-004'],
                    ['3100-0001', '4-0-02-004-03-001'],
                    ['4101', '5-0-02-001-02-007'],
                    ['4101-0001', '5-0-02-007-03-001'],
                    ['5202', '6-0-04-002-02-015'],
                    ['5202-0001', '6-0-04-015-03-001'],
                    ['1102', '1-0-02-001-02-002'],
                    ['1102-0001', '1-0-02-001-04-002'],
                    ['1102-0002', '1-0-02-001-04-001'],
                    ['2103', '2-0-02-000-01-001'],
                    ['2103-0001', '2-0-02-001-03-001'],
                    ['2104', '2-0-16-004-03-009'],
                    ['2104-0001', '2-0-16-004-04-003'],
                    ['3100', '4-0-02-001-02-004'],
                    ['3100-0001', '4-0-02-004-03-001'],
                    ['4101', '5-0-02-001-02-007'],
                    ['4101-0001', '5-0-02-007-03-001'],
                    ['1102', '1-0-02-001-02-002'],
                    ['1102-0001', '1-0-02-001-04-002'],
                    ['1102-0002', '1-0-02-001-04-001'],
                    ['1107', '2-0-16-004-03-009'],
                    ['1107-0001', '2-0-16-004-04-001'],
                    ['2101', '2-0-16-006-03-016'],
                    ['2101-0001', '2-0-16-016-04-008'],
                    ['2102', '2-0-16-001-02-006'],
                    ['2102-0001', '2-0-16-006-03-019'],
                    ['2103', '2-0-02-000-01-001'],
                    ['2103-0001', '2-0-02-001-03-001'],
                    ['2104', '2-0-16-004-03-009'],
                    ['2104-0001', '2-0-16-004-04-003'],
                    ['3100', '4-0-02-001-02-004'],
                    ['3100-0001', '4-0-02-004-03-001'],
                    ['4101', '5-0-02-001-02-007'],
                    ['4101-0001', '5-0-02-007-03-001'],
                    ['5202', '6-0-04-002-02-015'],
                    ['5202-0001', '6-0-04-015-03-001'],
                    ['1102', '1-0-02-001-02-002'],
                    ['1102-0001', '1-0-02-001-04-002'],
                    ['1102-0002', '1-0-02-001-04-001'],
                    ['1107', '2-0-16-004-03-009'],
                    ['1107-0001', '2-0-16-004-04-001'],
                    ['2101', '2-0-16-006-03-016'],
                    ['2101-0001', '2-0-16-016-04-008'],
                    ['2102', '2-0-16-001-02-006'],
                    ['2102-0001', '2-0-16-006-03-019'],
                    ['2103', '2-0-02-000-01-001'],
                    ['2103-0001', '2-0-02-001-03-001'],
                    ['2104', '2-0-16-004-03-009'],
                    ['2104-0001', '2-0-16-004-04-003'],
                    ['3100', '4-0-02-001-02-004'],
                    ['3100-0001', '4-0-02-004-03-001'],
                    ['4101', '5-0-02-001-02-007'],
                    ['4101-0001', '5-0-02-007-03-001'],
                    ['5202', '6-0-04-002-02-015'],
                    ['5202-0001', '6-0-04-015-03-001']]

        for cuenta in _cuentas:
            try:
                c = ContableCuenta.objects.get(codigo=cuenta[0])
            except Exception as ex:
                print(ex)
                # self.message_user(request, f"FAIL cuenta: {cuenta[0]}")
            c.long_code = cuenta[1]
            c.save()

    def get_id_tipo(self):
        return 1

    def get_queryset(self, request):
        return ContableCuenta.objects.all()

    def _codigo(self, obj):
        return _format_field_cuenta(obj, "long_code")

    def _nombre(self, obj):
        return _format_field_cuenta(obj, "sobrenombre")

    def _saldo_inicial(self, obj):
        es_cuenta_padre, saldo_inicial = obj.calcula_saldo_inicial()
        return _show_field(es_cuenta_padre, saldo_inicial)

    def _cargo(self, obj):
        id_tipo = self.get_id_tipo()
        es_cuenta_padre, cargo = obj.calcula_cargo(id_tipo)
        return _show_field(es_cuenta_padre, cargo)

    def _abono(self, obj):
        id_tipo = self.get_id_tipo()
        es_cuenta_padre, abono = obj.calcula_abono(id_tipo)
        return _show_field(es_cuenta_padre, abono)

    def _saldo(self, obj):
        id_tipo = self.get_id_tipo()
        es_cuenta_padre, saldo_final = obj.calcula_saldo_final(id_tipo)
        return _show_field(es_cuenta_padre, saldo_final)


"""
TRANSFERENCIA RECIBIDA --->>>
"""


class ContableCuentaTransferenciaRecibidaProxy(ContableCuenta):
    class Meta:
        proxy = True
        verbose_name_plural = "(Transferencia Recibida)"


class MovimientoRecibidaAdminInLine(MovimientoAdminInLine):
    def get_queryset(self, request):
        qs = super(MovimientoAdminInLine, self).get_queryset(request)
        return qs.filter(tipo=TipoContableCuenta.objects.get(id=1))


class ContableCuentaTransferenciaRecibidaAdmin(ContableCuentaAdmin):
    inlines = (MovimientoRecibidaAdminInLine, )

    def get_id_tipo(self):
        return 1

    def get_queryset(self, request):
        id_tipo = self.get_id_tipo()
        return balanza_get_queryset(id_tipo)


"""
TRANSFERENCIA ENVIADA --->>>
"""


class MovimientoEnviadaAdminInLine(MovimientoAdminInLine):
    def get_queryset(self, request):
        qs = super(MovimientoAdminInLine, self).get_queryset(request)
        return qs.filter(tipo=TipoContableCuenta.objects.get(id=2))


class ContableCuentaTransferenciaEnviadaProxy(ContableCuenta):
    class Meta:
        proxy = True
        verbose_name_plural = "(Transferencia Enviada)"


class ContableCuentaTransferenciaEnviadaAdmin(ContableCuentaAdmin):
    inlines = (MovimientoEnviadaAdminInLine, )

    def get_id_tipo(self):
        return 2

    def get_queryset(self, request):
        id_tipo = self.get_id_tipo()
        return balanza_get_queryset(id_tipo)


"""
DEPÓSITO EN EFECTIVO vía Scotiabank --->>>
"""


class MovimientoDepositoEfectivoSBAdminInLine(MovimientoAdminInLine):
    def get_queryset(self, request):
        qs = super(MovimientoAdminInLine, self).get_queryset(request)
        return qs.filter(tipo=TipoContableCuenta.objects.get(id=3))


class ContableCuentaDepositoEfectivoSBProxy(ContableCuenta):
    class Meta:
        proxy = True
        verbose_name_plural = "(Depósito Efectivo SB)"


class ContableCuentaDepositoEfectivoSBAdmin(ContableCuentaAdmin):
    inlines = (MovimientoDepositoEfectivoSBAdminInLine, )

    def get_id_tipo(self):
        return 3

    def get_queryset(self, request):
        id_tipo = self.get_id_tipo()
        return balanza_get_queryset(id_tipo)


"""
DEPÓSITO EN EFECTIVO (Socio Comercial) --->>>
"""


class MovimientoDepositoEfectivoSCAdminInLine(MovimientoAdminInLine):
    def get_queryset(self, request):
        qs = super(MovimientoAdminInLine, self).get_queryset(request)
        return qs.filter(tipo=TipoContableCuenta.objects.get(id=4))


class ContableCuentaDepositoEfectivoSCProxy(ContableCuenta):
    class Meta:
        proxy = True
        verbose_name_plural = "(Depósito Efectivo SC)"


class ContableCuentaDepositoEfectivoSCAdmin(ContableCuentaAdmin):
    inlines = (MovimientoDepositoEfectivoSCAdminInLine, )

    def get_id_tipo(self):
        return 4

    def get_queryset(self, request):
        id_tipo = self.get_id_tipo()
        return balanza_get_queryset(id_tipo)


"""
RETIRO EN EFECTIVO (Socio Comercial) --->>>
"""


class MovimientoRetiroEfectivoSCAdminInLine(MovimientoAdminInLine):
    def get_queryset(self, request):
        qs = super(MovimientoAdminInLine, self).get_queryset(request)
        return qs.filter(tipo=TipoContableCuenta.objects.get(id=5))


class ContableCuentaRetiroEfectivoSCProxy(ContableCuenta):
    class Meta:
        proxy = True
        verbose_name_plural = "(Retiro Efectivo SC)"


class ContableCuentaRetiroEfectivoSCAdmin(ContableCuentaAdmin):
    inlines = (MovimientoRetiroEfectivoSCAdminInLine, )

    def get_id_tipo(self):
        return 5

    def get_queryset(self, request):
        id_tipo = self.get_id_tipo()
        return balanza_get_queryset(id_tipo)


"""
RETIRO EN EFECTIVO (Scotia Bank) --->>>
"""


class MovimientoRetiroEfectivoSBAdminInLine(MovimientoAdminInLine):
    def get_queryset(self, request):
        qs = super(MovimientoAdminInLine, self).get_queryset(request)
        return qs.filter(tipo=TipoContableCuenta.objects.get(id=6))


class ContableCuentaRetiroEfectivoSBProxy(ContableCuenta):
    class Meta:
        proxy = True
        verbose_name_plural = "(Retiro Efectivo SB)"


class ContableCuentaRetiroEfectivoSBAdmin(ContableCuentaAdmin):
    inlines = (MovimientoRetiroEfectivoSBAdminInLine, )

    def get_id_tipo(self):
        return 6

    def get_queryset(self, request):
        id_tipo = self.get_id_tipo()
        return balanza_get_queryset(id_tipo)


"""
CODI --->>>
"""


class MovimientoRetiroEfectivoCODIAdminInLine(MovimientoAdminInLine):
    def get_queryset(self, request):
        qs = super(MovimientoAdminInLine, self).get_queryset(request)
        return qs.filter(tipo=TipoContableCuenta.objects.get(id=7))


class ContableCuentaRetiroEfectivoCODIProxy(ContableCuenta):
    class Meta:
        proxy = True
        verbose_name_plural = "(CODI)"


class ContableCuentaRetiroEfectivoCODIAdmin(ContableCuentaAdmin):
    inlines = (MovimientoRetiroEfectivoCODIAdminInLine, )

    def get_id_tipo(self):
        return 7

    def get_queryset(self, request):
        id_tipo = self.get_id_tipo()
        return balanza_get_queryset(id_tipo)


"""
DDE Invercratos --->>>
"""


class MovimientoRetiroEfectivoDDEInvercratosAdminInLine(MovimientoAdminInLine):
    def get_queryset(self, request):
        qs = super(MovimientoAdminInLine, self).get_queryset(request)
        return qs.filter(tipo=TipoContableCuenta.objects.get(id=8))


class ContableCuentaRetiroEfectivoDDEInvercratosProxy(ContableCuenta):
    class Meta:
        proxy = True
        verbose_name_plural = "(DDE Invercratos)"


class ContableCuentaRetiroEfectivoDDEInvercratosAdmin(ContableCuentaAdmin):
    inlines = (MovimientoRetiroEfectivoDDEInvercratosAdminInLine, )

    def get_id_tipo(self):
        return 8

    def get_queryset(self, request):
        id_tipo = self.get_id_tipo()
        return balanza_get_queryset(id_tipo)


"""
DDE INGUZ --->>>
"""


class MovimientoRetiroEfectivoDDEINGUZAdminInLine(MovimientoAdminInLine):
    def get_queryset(self, request):
        qs = super(MovimientoAdminInLine, self).get_queryset(request)
        return qs.filter(tipo=TipoContableCuenta.objects.get(id=9))


class ContableCuentaRetiroEfectivoDDEINGUZProxy(ContableCuenta):
    class Meta:
        proxy = True
        verbose_name_plural = "(DDE INGUZ)"


class ContableCuentaRetiroEfectivoDDEINGUZAdmin(ContableCuentaAdmin):
    inlines = (MovimientoRetiroEfectivoDDEINGUZAdminInLine, )

    def get_id_tipo(self):
        return 9

    def get_queryset(self, request):
        id_tipo = self.get_id_tipo()
        return balanza_get_queryset(id_tipo)


"""
BALANZA GENERAL --->>>
"""


class MovimientoBGAdminInLine(MovimientoAdminInLine):
    def get_queryset(self, request):
        qs = super(MovimientoAdminInLine, self).get_queryset(request)
        return qs


class ContableCuentaBGProxy(ContableCuenta):
    class Meta:
        proxy = True
        verbose_name_plural = "(BALANZA GENERAL)"


class ContableCuentaBGAdmin(ContableCuentaAdmin):
    inlines = (MovimientoBGAdminInLine, )

    def get_id_tipo(self):
        return 9

    def get_queryset(self, request):
        return ContableCuenta.objects.all().order_by('orden_admin')

    def _codigo(self, obj):
        return _format_field_cuenta(obj, "long_code")

    def _nombre(self, obj):
        return _format_field_cuenta(obj, "sobrenombre")

    def _saldo_inicial(self, obj):
        es_cuenta_padre, saldo_inicial = obj.calcula_saldo_inicial()
        return _show_field(es_cuenta_padre, saldo_inicial)

    def _cargo(self, obj):
        id_tipo = self.get_id_tipo()
        es_cuenta_padre, cargo = obj.calcula_cargo(id_tipo)
        return _show_field(es_cuenta_padre, cargo)

    def _abono(self, obj):
        id_tipo = self.get_id_tipo()
        es_cuenta_padre, abono = obj.calcula_abono(id_tipo)
        return _show_field(es_cuenta_padre, abono)

    def _saldo(self, obj):
        id_tipo = self.get_id_tipo()
        es_cuenta_padre, saldo_final = obj.calcula_saldo_final(id_tipo)
        return _show_field(es_cuenta_padre, saldo_final)


"""
-------------------------------------------------------------------
"""


class CuentaTipoInline(admin.TabularInline):
    model = TipoContableCuenta.cuentas.through
    verbose_name_plural = 'Cuentas'
    extra = 0
    ordering = ['cuenta__codigo', ]
    fields = ['_codigo',
              'cuenta',
              'regla_cargo',
              'regla_abono']

    readonly_fields = ['_codigo']

    def _codigo(self, obj):
        return obj.cuenta.codigo


class TipoContableCuentaAdmin(admin.ModelAdmin):
    model = TipoContableCuenta
    fields = [
        'tipo',
        'activo']
    inlines = [CuentaTipoInline, ]


"""
INGUZ INGUZ Enviada
"""


class MovimientoEnviadoInguzInguzInLine(MovimientoAdminInLine):
    def get_queryset(self, request):
        qs = super(MovimientoAdminInLine, self).get_queryset(request)
        return qs.filter(tipo=TipoContableCuenta.objects.get(id=16))


class ContableCuentaEnviadoInguzInguzProxy(ContableCuenta):
    class Meta:
        proxy = True
        verbose_name_plural = "(INGUZ INGUZ Enviada)"


class EnviadoInguzInguzAdmin(ContableCuentaAdmin):
    inlines = (MovimientoRetiroEfectivoDDEINGUZAdminInLine, )

    def get_id_tipo(self):
        return 16

    def get_queryset(self, request):
        id_tipo = self.get_id_tipo()
        return balanza_get_queryset(id_tipo)


"""
INGUZ INGUZ Recibida
"""


class MovimientoRecibidaInguzInguzInLine(MovimientoAdminInLine):
    def get_queryset(self, request):
        qs = super(MovimientoAdminInLine, self).get_queryset(request)
        return qs.filter(tipo=TipoContableCuenta.objects.get(id=15))


class ContableCuentaRecibidaInguzInguzProxy(ContableCuenta):
    class Meta:
        proxy = True
        verbose_name_plural = "(INGUZ INGUZ Recibida)"


class RecibidaInguzInguzAdmin(ContableCuentaAdmin):
    inlines = (MovimientoRetiroEfectivoDDEINGUZAdminInLine, )

    def get_id_tipo(self):
        return 15

    def get_queryset(self, request):
        id_tipo = self.get_id_tipo()
        return balanza_get_queryset(id_tipo)


admin.site.register(CuentaSaldo, CuentaSaldoAdmin)
# admin.site.register(ContableCuenta, ContableCuentaAdmin)
admin.site.register(TipoContableCuenta, TipoContableCuentaAdmin)
admin.site.register(ContableCuentaTransferenciaRecibidaProxy,
                    ContableCuentaTransferenciaRecibidaAdmin)
admin.site.register(ContableCuentaTransferenciaEnviadaProxy,
                    ContableCuentaTransferenciaEnviadaAdmin)
admin.site.register(ContableCuentaDepositoEfectivoSBProxy,
                    ContableCuentaDepositoEfectivoSBAdmin)
admin.site.register(ContableCuentaDepositoEfectivoSCProxy,
                    ContableCuentaDepositoEfectivoSCAdmin)
admin.site.register(ContableCuentaRetiroEfectivoSCProxy,
                    ContableCuentaRetiroEfectivoSCAdmin)
admin.site.register(ContableCuentaRetiroEfectivoSBProxy,
                    ContableCuentaRetiroEfectivoSBAdmin)
admin.site.register(ContableCuentaRetiroEfectivoCODIProxy,
                    ContableCuentaRetiroEfectivoCODIAdmin)
admin.site.register(ContableCuentaEnviadoInguzInguzProxy,
                    EnviadoInguzInguzAdmin)
admin.site.register(ContableCuentaRecibidaInguzInguzProxy,
                    RecibidaInguzInguzAdmin)
# admin.site.register(ContableCuentaRetiroEfectivoDDEInvercratosProxy,
#                     ContableCuentaRetiroEfectivoDDEInvercratosAdmin)
# admin.site.register(ContableCuentaRetiroEfectivoDDEINGUZProxy,
#                     ContableCuentaRetiroEfectivoDDEINGUZAdmin)
admin.site.register(ContableCuentaBGProxy,
                    ContableCuentaBGAdmin)
admin.site.register(CuentaTipo)
admin.site.register(ContableMovimiento, MovimientosContaAdmin)
