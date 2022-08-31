from django.contrib import admin
from seguros.models import InfoSeguros


class InfoSegurosAdmin(admin.ModelAdmin):
    list_display = ('num_poliza', 'user')


admin.site.register(InfoSeguros, InfoSegurosAdmin)
