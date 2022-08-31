from django.contrib import admin
from banca.models.transaccion import (Transaccion,
                                      ValidacionSesion,
                                      ValidacionTransaccion,
                                      SaldoReservado)
from banca.models import InguzTransaction
from spei.models import StpTransaction
from banca.models.comisionSTP import ComisioneSTP
from pld.models.movements import Movimiento
from banca.models.regulacion import ValidacionRegulatoria
from banca.models.catalogos import ErroresTransaccion
from rangefilter.filter import DateTimeRangeFilter


class MovimientoInline(admin.StackedInline):
    model = Movimiento
    can_delete = False
    verbose_name_plural = 'Movimiento PLD'
    fk_name = 'transaccion'


class ValidacionSesionInline(admin.StackedInline):
    model = ValidacionSesion
    can_delete = False
    verbose_name_plural = 'Validacion Sesion'
    fk_name = 'transaccion'


class ValidacionTransaccionInline(admin.StackedInline):
    model = ValidacionTransaccion
    can_delete = False
    verbose_name_plural = 'Validacion Transaccion'
    fk_name = 'transaccion'


class ComisioneSTPInline(admin.StackedInline):
    model = ComisioneSTP
    can_delete = False
    verbose_name_plural = 'Comision STP'
    fk_name = 'transaccion'


class StpTransactionInline(admin.StackedInline):
    model = StpTransaction
    can_delete = False
    verbose_name_plural = 'STP'
    fk_name = 'transaccion'


class ValidacionRegulatoriaInline(admin.StackedInline):
    model = ValidacionRegulatoria
    can_delete = False
    verbose_name_plural = 'Validacion regulatoria'
    fk_name = 'transaccion'


class InguzInline(admin.StackedInline):
    model = InguzTransaction
    can_delete = False
    verbose_name_plural = 'Inguz'
    fk_name = 'transaccion'


class TransaccionAdmin(admin.ModelAdmin):
    inlines = (
        ValidacionSesionInline,
        ValidacionTransaccionInline,
        StpTransactionInline,
        ComisioneSTPInline,
        MovimientoInline,
        ValidacionRegulatoriaInline,
        InguzInline,
        )

    search_fields = ('id',
                     'monto',
                     'user__username',
                     'user__id',
                     )

    list_filter = ('tipoTrans',
                   ('fechaAplicacion', DateTimeRangeFilter),
                   ('fechaValor', DateTimeRangeFilter),
                   'statusTrans',
                   'errorRes',
                   'tipoTrans',
                   )

    list_display = ('id',
                    'user',
                    'fechaValor',
                    'fechaAplicacion',
                    'monto',
                    'statusTrans',
                    'errorRes',
                    'tipoTrans',
                    )

    list_per_page = 25

    #
    # def get_estado(self, obj):
    #     return obj.Uprofile.status
    # get_estado.short_description = 'Estado'
    #
    # def get_curp(self, obj):
    #     return obj.Uprofile.curp
    # get_curp.short_description = 'Check CURP'
    #
    # def get_rfc(self, obj):
    #     return obj.Uprofile.rfc
    # get_rfc.short_description = 'Check RFC'
    #


class ErroresAdmin(admin.ModelAdmin):
    list_display = ('mensaje',
                    'codigo')


class SaldoReservadoAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SaldoReservado._meta.fields]
    readonly_fields = (
        'tipoTrans',
        'fecha_reservado',
        'fecha_aplicado_devuelto',
        'saldo_reservado',
    )


admin.site.register(SaldoReservado, SaldoReservadoAdmin)
admin.site.register(Transaccion, TransaccionAdmin)

admin.site.register(ErroresTransaccion, ErroresAdmin)
