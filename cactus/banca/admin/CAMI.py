from django.contrib import admin
from banca.models import CAMI


class CAMIAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo')

    list_filter = ('tipo',
                   )


admin.site.register(CAMI, CAMIAdmin)
