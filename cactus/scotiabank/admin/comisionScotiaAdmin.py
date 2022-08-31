from django.contrib import admin
from scotiabank.models import ComisionesScotia


class ComisionesScotiaAdmin(admin.ModelAdmin):

    readonly_fields = (
        'iva',
        'comision_total',
    )
    list_display = (
        'transaccion',
        'comision_scotia',
        'iva',
        'comision_inguz',
        'comision_total',
    )

    def has_delete_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True


admin.site.register(ComisionesScotia, ComisionesScotiaAdmin)
