from django.contrib import admin
# from contabilidad.models.resumen import (CuentaPropia,
#                                          SubcuentaIVA,
#                                          SubcuentaSTPIVA,
#                                          CuentaTerceros,
#                                          CuentaSTP,
#                                          SCDTFTPE,
#                                          IVAacreditableNoPagado,
#                                          ComisionesporPagarSobreOperacionesVigentes,  # noqa: 501
#                                          IVAnoCobrado,
#                                          IVAcobrado,
#                                          ComisionesCobradas,
#                                          ComisionesPagadas,
#                                          FondosPagoElectronico
#                                          )
# Register your models here.


class CuentaPropiaAdmin(admin.ModelAdmin):
    list_display = ('saldoinicial', 'debe', 'haber', 'saldofinal', 'resumen')


class SubcuentaIVAAdmin(admin.ModelAdmin):
    list_display = ('saldoinicial', 'debe', 'haber', 'saldofinal', 'resumen')


class SubcuentaSTPIVAAdmin(admin.ModelAdmin):
    list_display = ('saldoinicial', 'debe', 'haber', 'saldofinal', 'resumen')


class CuentaTercerosAdmin(admin.ModelAdmin):
    list_display = ('saldoinicial', 'debe', 'haber', 'saldofinal', 'resumen')


class CuentaSTPAdmin(admin.ModelAdmin):
    list_display = ('saldoinicial', 'debe', 'haber', 'saldofinal', 'resumen')


class SCDTFTPEAdmin(admin.ModelAdmin):
    list_display = ('saldoinicial', 'debe', 'haber', 'saldofinal', 'resumen')


class IVAacreditableNoPagadoAdmin(admin.ModelAdmin):
    list_display = ('saldoinicial', 'debe', 'haber', 'saldofinal', 'resumen')


class ComisionesporPagarSobreOperacionesVigentesAdmin(admin.ModelAdmin):
    list_display = ('saldoinicial', 'debe', 'haber', 'saldofinal', 'resumen')


class IVAnoCobradoAdmin(admin.ModelAdmin):
    list_display = ('saldoinicial', 'debe', 'haber', 'saldofinal', 'resumen')


class IVAcobradoAdmin(admin.ModelAdmin):
    list_display = ('saldoinicial', 'debe', 'haber', 'saldofinal', 'resumen')


class ComisionesCobradasAdmin(admin.ModelAdmin):
    list_display = ('saldoinicial', 'debe', 'haber', 'saldofinal', 'resumen')


class ComisionesPagadasAdmin(admin.ModelAdmin):
    list_display = ('saldoinicial', 'debe', 'haber', 'saldofinal', 'resumen')


class FondosPagoElectronicoAdmin(admin.ModelAdmin):
    list_display = ('saldoinicial', 'debe', 'haber', 'saldofinal', 'resumen')


# admin.site.register(CuentaPropia, CuentaPropiaAdmin)
# admin.site.register(SubcuentaIVA, SubcuentaIVAAdmin)
# admin.site.register(SubcuentaSTPIVA, SubcuentaSTPIVAAdmin)
# admin.site.register(CuentaTerceros, CuentaTercerosAdmin)
# admin.site.register(CuentaSTP, CuentaSTPAdmin)
# admin.site.register(SCDTFTPE, SCDTFTPEAdmin)
# admin.site.register(IVAacreditableNoPagado, IVAacreditableNoPagadoAdmin)
# admin.site.register(ComisionesporPagarSobreOperacionesVigentes,
#                     ComisionesporPagarSobreOperacionesVigentesAdmin)
# admin.site.register(IVAnoCobrado, IVAnoCobradoAdmin)
# admin.site.register(IVAcobrado, IVAcobradoAdmin)
# admin.site.register(ComisionesCobradas, ComisionesCobradasAdmin)
# admin.site.register(ComisionesPagadas, ComisionesPagadasAdmin)
# admin.site.register(FondosPagoElectronico, FondosPagoElectronicoAdmin)
