from django.contrib import admin
from spei.models import (StpTransaction, StpInstitution,
                         InstitutionBanjico, adminUtils,
                         FolioStp, StpNotificacionEstadoDeCuenta)


class InstitutionBanjicoAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'short_id', 'long_id')
    # TODO cambiar display para mostrar nombres en español.


class adminUtilsAdmin(admin.ModelAdmin):
    list_display = ('util', 'activo')
    list_editable = ('activo',)


class StpTransactionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in StpTransaction._meta.fields]


admin.site.register(adminUtils, adminUtilsAdmin)
admin.site.register(StpTransaction, StpTransactionAdmin)
admin.site.register(StpInstitution)
admin.site.register(FolioStp)
admin.site.register(InstitutionBanjico, InstitutionBanjicoAdmin)
admin.site.register(StpNotificacionEstadoDeCuenta)
