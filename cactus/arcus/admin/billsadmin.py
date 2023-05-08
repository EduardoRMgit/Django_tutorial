from django.contrib import admin
from arcus.models import Bills, ServicesArcus, RecargasArcus
from arcus.utils.autharcus import headers_arcus
import requests
import json
from deep_translator import GoogleTranslator
from django.conf import settings


class BillsAdmin(admin.ModelAdmin):
    search_fields = ('user',
                     'bill_id',
                     'account_number',
                     'monto'
                     )
    list_filter = ('user',
                   'bill_id',
                   'account_number',
                   'monto'
                   )
    list_display = ('user',
                    'bill_id',
                    'account_number',
                    'monto'
                    )


class ServicesArcusAdmin(admin.ModelAdmin):
    actions = ["updateservices"]
    search_fields = ('id_bill',
                     'name',
                     'biller_type'
                     )
    list_filter = ('id_bill',
                   'name',
                   'biller_type'
                   )
    list_display = ('id_bill',
                    'name',
                    'biller_type',
                    'bill_type',
                    'country',
                    'currency',
                    'requires_name_on_account',
                    'hours_to_fulfill',
                    'account_number_digits',
                    'mask',
                    'can_check_balance',
                    'supports_partial_payments',
                    'has_xdata'
                    )

    def updateservices(self, request, servicios):
        headers = headers_arcus("/billers/utilities")
        url = f"{settings.ARCUS_DOMAIN}/billers/utilities"
        servicios = (requests.get(url=url, headers=headers)).content.decode()
        print(servicios)
        servicios = (json.loads(servicios))["billers"]
        gs = GoogleTranslator(source='en', target='es')
        for servicio in servicios:
            tipo = gs.translate(servicio["biller_type"])
            valida = ServicesArcus.objects.filter(
                id_bill=servicio["id"]).count()
            if valida:
                ServicesArcus.objects.filter(
                    id_bill=servicio["id"]).update(
                        id_bill=servicio["id"],
                        name=servicio["name"],
                        biller_type=tipo,
                        bill_type=servicio["bill_type"],
                        country=servicio["country"],
                        currency=servicio["currency"],
                        requires_name_on_account=servicio[
                            "requires_name_on_account"],
                        hours_to_fulfill=servicio["hours_to_fulfill"],
                        account_number_digits=servicio[
                            "account_number_digits"],
                        mask=servicio["mask"],
                        can_check_balance=servicio["can_check_balance"],
                        supports_partial_payments=servicio[
                            "supports_partial_payments"],
                        has_xdata=servicio["has_xdata"])
            else:
                ServicesArcus.objects.create(
                    id_bill=servicio["id"],
                    name=servicio["name"],
                    biller_type=tipo,
                    bill_type=servicio["bill_type"],
                    country=servicio["country"],
                    currency=servicio["currency"],
                    requires_name_on_account=servicio[
                            "requires_name_on_account"],
                    hours_to_fulfill=servicio["hours_to_fulfill"],
                    account_number_digits=servicio[
                            "account_number_digits"],
                    mask=servicio["mask"],
                    can_check_balance=servicio["can_check_balance"],
                    supports_partial_payments=servicio[
                        "supports_partial_payments"],
                    has_xdata=servicio["has_xdata"])


class RecargasArcusAdmin(admin.ModelAdmin):
    actions = ["updaterecargas"]
    search_fields = ('id_recarga',
                     'name',
                     'biller_type'
                     )
    list_filter = ('id_recarga',
                   'name',
                   'biller_type'
                   )
    list_display = ('id_recarga',
                    'name',
                    'biller_type',
                    'bill_type',
                    'country',
                    'currency',
                    'requires_name_on_account',
                    'hours_to_fulfill',
                    'account_number_digits',
                    'mask',
                    'can_check_balance',
                    'supports_partial_payments',
                    'has_xdata',
                    'available_topup_amounts',
                    'topup_commission'
                    )

    def updaterecargas(self, request, servicios):
        headers = headers_arcus("/billers/topups")
        url = f"{settings.ARCUS_DOMAIN}/billers/topups"
        recargas = (requests.get(url=url, headers=headers)).content.decode()
        recargas = (json.loads(recargas))["billers"]
        print(recargas)
        gs = GoogleTranslator(source='en', target='es')
        for recarga in recargas:
            tipo = gs.translate(recarga["biller_type"])
            valida = RecargasArcus.objects.filter(
                id_recarga=recarga["id"]).count()
            if valida:
                RecargasArcus.objects.filter(
                    id_recarga=recarga["id"]).update(
                        id_recarga=recarga["id"],
                        name=recarga["name"],
                        biller_type=tipo,
                        bill_type=recarga["bill_type"],
                        country=recarga["country"],
                        currency=recarga["currency"],
                        requires_name_on_account=recarga[
                            "requires_name_on_account"],
                        hours_to_fulfill=recarga["hours_to_fulfill"],
                        account_number_digits=recarga[
                            "account_number_digits"],
                        mask=recarga["mask"],
                        can_check_balance=recarga["can_check_balance"],
                        supports_partial_payments=recarga[
                            "supports_partial_payments"],
                        has_xdata=recarga["has_xdata"],
                        available_topup_amounts=recarga[
                            "available_topup_amounts"],
                        topup_commission=recarga["topup_commission"]
                        )
            else:
                RecargasArcus.objects.create(
                    id_recarga=recarga["id"],
                    name=recarga["name"],
                    biller_type=tipo,
                    bill_type=recarga["bill_type"],
                    country=recarga["country"],
                    currency=recarga["currency"],
                    requires_name_on_account=recarga[
                            "requires_name_on_account"],
                    hours_to_fulfill=recarga["hours_to_fulfill"],
                    account_number_digits=recarga[
                            "account_number_digits"],
                    mask=recarga["mask"],
                    can_check_balance=recarga["can_check_balance"],
                    supports_partial_payments=recarga[
                        "supports_partial_payments"],
                    has_xdata=recarga["has_xdata"],
                    available_topup_amounts=recarga[
                            "available_topup_amounts"],
                    topup_commission=recarga["topup_commission"])


admin.site.register(Bills, BillsAdmin)
admin.site.register(ServicesArcus, ServicesArcusAdmin)
admin.site.register(RecargasArcus, RecargasArcusAdmin)
