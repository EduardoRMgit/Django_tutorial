from django.contrib import admin
from arcus.models import Bills, ServicesArcus, RecargasArcus, TiempoAire
from arcus.utils.autharcus import headers_arcus
from arcus.utils.categorias import categorias
import requests
import json
from django.conf import settings
import logging

db_logger = logging.getLogger('db')


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
    search_fields = ('sku_id',
                     'name',
                     'biller_type'
                     )
    list_filter = ('sku_id',
                   'name',
                   'biller_type'
                   )
    list_display = ('sku_id',
                    'name',
                    'biller_type',
                    'country',
                    'bill_types',
                    'currency',
                    'customer_fee',
                    'customer_fee_type',
                    'logo_url',
                    'autopay',
                    'tracking',
                    'supports_partial_payments',
                    'hours_to_fulfill',
                    'allows_reversal'
                    )

    def updateservices(self, request, servicios):
        headers = headers_arcus()
        url = f"{settings.ARCUS_DOMAIN}/merchants"
        try:
            servicios = (
                requests.get(url=url, headers=headers)).content.decode()
            servicios = (json.loads(servicios))["merchants"]
            for servicio in servicios:
                tipo = categorias(servicio["biller_type"], servicio["name"])
                valida = ServicesArcus.objects.filter(
                    sku_id=servicio["sku"]).count()
                if valida:
                    ServicesArcus.objects.filter(
                        sku_id=servicio["sku"]).update(
                            sku_id=servicio["sku"],
                            name=servicio["name"],
                            biller_type=tipo,
                            bill_types=servicio["bill_types"],
                            country=servicio["country"],
                            currency=servicio["currency"],
                            customer_fee=servicio[
                                "customer_fee"],
                            customer_fee_type=servicio[
                                "customer_fee_type"],
                            logo_url=servicio["logo_url"],
                            autopay=servicio["autopay"],
                            tracking=servicio["tracking"],
                            supports_partial_payments=servicio[
                                "supports_partial_payments"],
                            hours_to_fulfill=servicio["hours_to_fulfill"],
                            allows_reversal=servicio["allows_reversal"])
                else:
                    ServicesArcus.objects.create(
                        sku_id=servicio["sku"],
                        name=servicio["name"],
                        biller_type=tipo,
                        bill_types=servicio["bill_types"],
                        country=servicio["country"],
                        currency=servicio["currency"],
                        customer_fee=servicio[
                            "customer_fee"],
                        customer_fee_type=servicio[
                            "customer_fee_type"],
                        logo_url=servicio["logo_url"],
                        autopay=servicio["autopay"],
                        tracking=servicio["tracking"],
                        supports_partial_payments=servicio[
                            "supports_partial_payments"],
                        hours_to_fulfill=servicio["hours_to_fulfill"],
                        allows_reversal=servicio["allows_reversal"])
                    print("a")
            msg_logg = "{}".format(
                "[ARCUS REQUEST] (get) actualizacion exitosa")
            db_logger.info(msg_logg)
        except Exception as error:
            msg = "[ARCUS REQUEST ERROR] get (ex:{}) (request:{})".format(
                error,
                servicios)
            db_logger.error(msg)


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
        try:
            headers = headers_arcus("/billers/topups")
            url = f"{settings.ARCUS_DOMAIN}/billers/topups"
            recargas = (
                requests.get(url=url, headers=headers)).content.decode()
            recargas = (json.loads(recargas))["billers"]
            for recarga in recargas:
                tipo = categorias(recarga["biller_type"], recarga["name"])
                if len(tipo) == 2:
                    name = tipo[1]
                    tipo = tipo[0]
                else:
                    name = recarga["name"]
                valida = RecargasArcus.objects.filter(
                    id_recarga=recarga["id"]).count()
                if valida:
                    RecargasArcus.objects.filter(
                        id_recarga=recarga["id"]).update(
                            id_recarga=recarga["id"],
                            name=name,
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
            msg_logg = "{}".format(
                "[ARCUS REQUEST] (get) actualizacion exitosa")
            db_logger.info(msg_logg)
        except Exception as error:
            msg = "[ARCUS REQUEST ERROR] get (ex:{}) (request:{})".format(
                error,
                servicios)
            db_logger.error(msg)


class TiempoAireAdmin(admin.ModelAdmin):
    search_fields = ('id',
                     'id_transaccion',
                     'transaccion',
                     'monto')
    list_filter = ('id',
                   'id_transaccion',
                   'transaccion',
                   'monto')
    list_display = ('id',
                    'transaccion',
                    'monto',
                    'moneda',
                    'monto_usd',
                    'comision',
                    'total_usd',
                    'fecha_creacion',
                    'estatus',
                    'id_externo',
                    'descripcion',
                    'numero_telefono',
                    )


admin.site.register(Bills, BillsAdmin)
admin.site.register(ServicesArcus, ServicesArcusAdmin)
admin.site.register(RecargasArcus, RecargasArcusAdmin)
admin.site.register(TiempoAire, TiempoAireAdmin)
