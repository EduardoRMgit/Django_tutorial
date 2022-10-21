from django.contrib import admin
from django.contrib import messages
import json
from dapp.models import PaymentInfo, Payments, StoreInfo, CreatePayment
from dapp.utility.peticiones import Peticiones


class PaymentInfoAdmin(admin.ModelAdmin):
    model = PaymentInfo
    list_display = [
        'qr',
        'qr_description',
        'qr_amount',
        'qr_reference_num',
    ]
    readonly_fields = [
        'qr_description',
        'qr_amount',
        'qr_currency',
        'qr_reference_num',
        'cashout_amount',
        'cashout_currency',
        'merchant_name',
        'merchant_address',
        'merchant_image',
        'merchant_type',
        'category_id',
        'category_name',
        'response',
    ]

    actions = ['get_PaymentInfo']

    def get_PaymentInfo(self, request, objetos):
        for objeto in objetos:
            peticion = Peticiones()
            qr = objeto.qr
            respuesta = peticion.paymentInfo(qr=qr)
            contenido = respuesta.content
            mensaje = "status code: " + str(respuesta.status_code) + " | "
            if respuesta.status_code == 200:
                objeto.response = json.loads(contenido)
                objeto.save()
                mensaje += "msg: " + (json.loads(contenido)['msg'])
            else:
                messages.error(request, mensaje)
            messages.info(request, mensaje)
    get_PaymentInfo.short_description = "obtener información de cobro"


class PaymentsAdmin(admin.ModelAdmin):
    model = Payments

    list_display = [
        'payment_id',
        'payment_reference',
    ]
    readonly_fields = [
        'response',
    ]

    actions = ['get_Payments']

    def get_Payments(self, request, objetos):
        for objeto in objetos:
            peticion = Peticiones()
            if objeto.payment_id and objeto.payment_reference:
                respuesta = peticion.payments(
                    id=objeto.payment_id,
                    reference=objeto.payment_reference
                )
            elif objeto.payment_id:
                respuesta = peticion.payments(
                    id=objeto.payment_id,
                )
            elif objeto.payment_reference:
                respuesta = peticion.payments(
                    reference=objeto.payment_reference
                )
            contenido = respuesta.content
            mensaje = "status code: " + str(respuesta.status_code) + " | "
            if respuesta.status_code == 200:
                objeto.response = json.loads(contenido)
                objeto.save()
                mensaje += "msg: " + (json.loads(contenido)['msg'])
            else:
                messages.error(request, mensaje)
            messages.info(request, mensaje)
    get_Payments.short_description = "obtener información de pago"


class StoreInfoAdmin(admin.ModelAdmin):
    model = StoreInfo

    list_display = [
        'latitude',
        'longitude',
        'radius'
    ]
    readonly_fields = [
        'response',
    ]

    actions = ['get_StoreInfo']

    def get_StoreInfo(self, request, objetos):
        for objeto in objetos:
            peticion = Peticiones()
            if objeto.radius:
                respuesta = peticion.storeInfo(
                    latitude=objeto.latitude,
                    longitude=objeto.longitude,
                    radio=objeto.radius
                )
            else:
                respuesta = peticion.storeInfo(
                    latitude=objeto.latitude,
                    longitude=objeto.longitude
                )
            contenido = respuesta.content
            print(contenido)
            mensaje = "status code: " + str(respuesta.status_code) + " | "
            if respuesta.status_code == 200:
                objeto.response = json.loads(contenido)
                objeto.save()
                mensaje += "msg: " + (json.loads(contenido)['msg'])
            else:
                messages.error(request, mensaje)
            messages.info(request, mensaje)
    get_StoreInfo.short_description = "obtener información de tiendas"


class CreatePaymentAdmin(admin.ModelAdmin):
    model = CreatePayment

    list_display = [
        'code',
        'name',
        'description',
        'amount'
    ]
    readonly_fields = [
        'response',
    ]

    actions = ['get_CreatePayment']

    def get_CreatePayment(self, request, objetos):
        for objeto in objetos:
            peticion = Peticiones()
            kwargs = {}
            kwargs["code"] = objeto.code
            kwargs["amount"] = str(objeto.amount)
            kwargs["description"] = objeto.description
            if objeto.name:
                kwargs["name"] = objeto.name
            if objeto.mail:
                kwargs["mail"] = objeto.mail
            if objeto.phone:
                kwargs["phone"] = objeto.phone
            if objeto.reference:
                kwargs["reference"] = objeto.reference
            if objeto.cashout_amount:
                kwargs["cash_amount"] = str(objeto.cashout_amount)
            print(kwargs)
            respuesta = peticion.createPayment(**kwargs)
            contenido = respuesta.content
            print(contenido)
            mensaje = "status code: " + str(respuesta.status_code) + " | "
            if respuesta.status_code == 200:
                objeto.response = json.loads(contenido)
                objeto.save()
                mensaje += "msg: " + (json.loads(contenido)['msg'])
            else:
                messages.error(request, mensaje)
            messages.info(request, mensaje)
    get_CreatePayment.short_description = "Realizar pago"


admin.site.register(PaymentInfo, PaymentInfoAdmin)
admin.site.register(Payments, PaymentsAdmin)
admin.site.register(StoreInfo, StoreInfoAdmin)
admin.site.register(CreatePayment, CreatePaymentAdmin)
