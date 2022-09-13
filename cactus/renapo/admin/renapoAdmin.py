from django.contrib import admin
from renapo.models import Renapo
from ..renapo_call import check_renapo
from demograficos.models.profileChecks import InfoValidator


class RenapoAdmin(admin.ModelAdmin):

    model = Renapo

    list_display = ['user',
                    'get_curp',
                    'exitoso']
    readonly_fields = (
        "curp",
        "renapo_resp",
        "renapo_nombre",
        "renapo_ap_pat",
        "renapo_ap_mat",
        "renapo_nacimiento",
        "msjError",
        "exitoso"
    )
    actions = ['renapo_call']

    search_fields = ("user_id", "curp")

    def get_curp(self, obj):
        obj.curp = obj.user.Uprofile.curp
        obj.save()
        print(obj.user.Uprofile.curp)
        return obj.user.Uprofile.curp
    get_curp.short_description = 'CURP'

    def renapo_call(self, request, instance):
        for elemento in instance:
            data, mensaje = check_renapo(elemento.curp)
            if data:
                valida, mensaje = InfoValidator.CURPValidado(
                    elemento.curp, elemento.user)
                if valida:
                    elemento.user.Uprofile.verificacion_curp = True
            else:
                elemento.user.Uprofile.verificacion_curp = False
            elemento.user.save()
            self.message_user(request, mensaje)
    renapo_call.short_description = 'llamada a RENAPO'


admin.site.register(Renapo, RenapoAdmin)
