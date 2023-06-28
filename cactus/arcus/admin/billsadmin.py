from django.contrib import admin
from arcus.models import Bills, ServicesArcus, RecargasArcus, PagosArcus
from arcus.utils.autharcus import headers_arcus
from arcus.utils.categorias import categorias
from arcus.utils.sftp import sftp_connect
import requests
import json
from django.conf import settings
import logging
import uuid

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

    def get_queryset(Self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.exclude(biller_type="NO MOSTRAR")
        return queryset

    def updateservices(self, request, servicios):
        uid = str(uuid.uuid4())
        headers = headers_arcus(uid)
        url = f"{settings.ARCUS_DOMAIN}/merchants"
        try:
            servicios = (
                requests.get(url=url, headers=headers)).content.decode()
            servicios = (json.loads(servicios))["merchants"]
            for servicio in servicios:
                tipo = categorias(servicio["biller_type"], servicio["name"])
                valida = ServicesArcus.objects.filter(
                    sku_id=servicio["sku"]).count()
                if servicio["sku"] == "4001771023":
                    servicio["name"] = "Dish [Código de barras]"
                if servicio["sku"] == "4000038028":
                    servicio["name"] = "Dish [Número de cuenta]"
                if servicio["sku"] == "4013646023":
                    servicio["name"] = "CESPE [Código de barras]"
                if servicio["sku"] == "4013649027":
                    servicio["name"] = "CESPE [Número de cuenta]"
                servicio["name"] = servicio["name"].replace(
                    "[Barcode]", "[Código de barras]")
                servicio["name"] = servicio["name"].replace(
                    "[BARCODE]", "[Código de barras]")
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
                    'bill_type',
                    'country',
                    'currency',
                    'customer_fee',
                    'customer_fee_type',
                    'logo_url',
                    'mask',
                    'topup_amounts',
                    'reference_lenght',
                    'carrier'
                    )

    def updaterecargas(self, request, servicios):
        try:
            uid = str(uuid.uuid4())
            headers = headers_arcus(uid)
            url = f"{settings.ARCUS_DOMAIN}/merchants/topups"
            recargas = (
                requests.get(url=url, headers=headers)).content.decode()
            recargas = (json.loads(recargas))["merchants"]
            for recarga in recargas:
                tipo = categorias(recarga["biller_type"], recarga["name"])
                if len(tipo) == 2:
                    name = tipo[1]
                    tipo = tipo[0]
                else:
                    name = recarga["name"]
                valida = RecargasArcus.objects.filter(
                    sku_id=recarga["sku"]).count()
                if valida:
                    RecargasArcus.objects.filter(
                        sku_id=recarga["sku"]).update(
                            sku_id=recarga["sku"],
                            name=name,
                            biller_type=tipo,
                            bill_type=recarga["bill_type"],
                            country=recarga["country"],
                            currency=recarga["currency"],
                            customer_fee=recarga["customer_fee"],
                            customer_fee_type=recarga["customer_fee_type"],
                            logo_url=recarga["logo_url"],
                            mask=recarga["mask"],
                            topup_amounts=recarga["topup_amounts"],
                            reference_lenght=recarga["reference_length"],
                            carrier=recarga["carrier"]
                            )
                else:
                    RecargasArcus.objects.create(
                        sku_id=recarga["sku"],
                        name=name,
                        biller_type=tipo,
                        bill_type=recarga["bill_type"],
                        country=recarga["country"],
                        currency=recarga["currency"],
                        customer_fee=recarga["customer_fee"],
                        customer_fee_type=recarga["customer_fee_type"],
                        logo_url=recarga["logo_url"],
                        mask=recarga["mask"],
                        topup_amounts=recarga["topup_amounts"],
                        reference_lenght=recarga["reference_length"],
                        carrier=recarga["carrier"])
            msg_logg = "{}".format(
                "[ARCUS REQUEST] (get) actualizacion exitosa")
            db_logger.info(msg_logg)
        except Exception as error:
            msg = "[ARCUS REQUEST ERROR] get (ex:{}) (request:{})".format(
                error,
                servicios)
            db_logger.error(msg)


class PagosArcusAdmin(admin.ModelAdmin):
    actions = ['conciliacion_pago']
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
                    'identificador',
                    'comision',
                    'fecha_creacion',
                    'estatus',
                    'id_externo',
                    'descripcion',
                    'numero_cuenta',
                    'tipo'
                    )

    def conciliacion_pago(self, request, pago):
        try:
            sftp_connect()
        except Exception as ex:
            msg = f"[ARCUS CONCILIACION ERROR] {ex}"
            db_logger.error(msg)


admin.site.register(Bills, BillsAdmin)
admin.site.register(ServicesArcus, ServicesArcusAdmin)
admin.site.register(RecargasArcus, RecargasArcusAdmin)
admin.site.register(PagosArcus, PagosArcusAdmin)
