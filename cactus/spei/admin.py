from django.contrib import admin
from django.contrib import messages
from spei.models import (StpTransaction,
                         StpInstitution,
                         InstitutionBanjico,
                         adminUtils,
                         FolioStp,
                         StpNotificacionEstadoDeCuenta,
                         MovimientoConciliacion,
                         ConciliacionSTP)
from .conciliacionSTP import conciliacion_stp


class InstitutionBanjicoAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'short_id', 'long_id')
    # TODO cambiar display para mostrar nombres en español.


class adminUtilsAdmin(admin.ModelAdmin):
    list_display = ('util', 'activo')
    list_editable = ('activo',)


class StpTransactionAdmin(admin.ModelAdmin):

    x = [f.name for f in StpTransaction._meta.fields]
    x.append("get_conciliado")
    list_display = x

    def get_conciliado(self, obj):
        return obj.StpConciliada
    get_conciliado.short_description = "Conciliado"


class MovimientoConciliacionAdmin(admin.ModelAdmin):
    list_display = (
        'idEF',
        'claveRastreo',
        'estado',
        'get_tipo',
        'get_fecha',
        'conciliada'
    )

    list_filter = ("conciliacion", "estado", "fechaOperacion", "estado")

    readonly_fields = [f.name for f in MovimientoConciliacion._meta.fields]

    def get_fecha(self, obj):
        return obj.fechaOperacion
    get_fecha.short_description = 'Fecha de la operación'

    def get_tipo(self, obj):
        if obj.conciliacion.tipo_orden_conciliacion == "R":
            return "Recibida"
        if obj.conciliacion.tipo_orden_conciliacion == "E":
            return "Enviada"
    get_tipo.short_description = 'Tipo de orden'


class MovimientoConciliaciionInline(admin.TabularInline):
    model = MovimientoConciliacion
    can_delete = False
    verbose_name_plural = 'Movimientos Conciliacion STP'
    fk_name = 'conciliacion'
    extra = 0
    readonly_fields = [f.name for f in MovimientoConciliacion._meta.fields]


class ConciliacionSTPAdmin(admin.ModelAdmin):
    inlines = (MovimientoConciliaciionInline,)
    list_display = (
        'fecha_inicio',
        'fecha_fin',
        'tipo_orden_conciliacion',
        "conciliado",
        "hora_de_conciliacion",
        "get_numMov"
    )
    actions = ['conciliacionSTP']

    readonly_fields = ("conciliado", "hora_de_conciliacion")

    def get_numMov(self, obj):
        num = MovimientoConciliacion.objects.filter(
            conciliacion=obj.id).count()
        return str(num)
    get_numMov.short_description = "Número de movimientos"

    def conciliacionSTP(self, request, objetos):
        """ Consula de transacciones STP para conciliación. """
        for objeto in objetos:
            mensaje = conciliacion_stp(objeto)
        messages.error(request, mensaje)
    conciliacionSTP.short_description = "Conciliación"


admin.site.register(adminUtils, adminUtilsAdmin)
admin.site.register(StpTransaction, StpTransactionAdmin)
admin.site.register(StpInstitution)
admin.site.register(FolioStp)
admin.site.register(InstitutionBanjico, InstitutionBanjicoAdmin)
admin.site.register(StpNotificacionEstadoDeCuenta)
admin.site.register(MovimientoConciliacion, MovimientoConciliacionAdmin)
admin.site.register(ConciliacionSTP, ConciliacionSTPAdmin)
