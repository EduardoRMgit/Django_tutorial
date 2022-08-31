from django.contrib import admin
from pld.models import Movimiento
from pld.utils.movements import llamada
from django.urls import path
import pandas as pd
from django.http import HttpResponseRedirect


class MovimientoAdmin(admin.ModelAdmin):
    change_list_template = "boton/movimiento.html"
    list_display = (
        'id',
        'id_entidad',
        'id_credito',
        'origen_pago',
        'tipo_cargo',
        'tipo_cargo_e',
        'monto_pago',
        'tipo_moneda',
        'fecha_pago',
        'payment_made_by',
        'status_code',
        'mensaje',
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path('movimiento/', self.get_movimiento)]
        return my_urls + urls

    def get_movimiento(self, request):
        try:
            csv = request.FILES['movimiento']
        except Exception:
            self.message_user(request, "Asegurate de cargar un archivo")
            return HttpResponseRedirect("../")
        self.upload_movimiento(csv, request)
        return HttpResponseRedirect("../")

    def upload_movimiento(self, file, request):
        if request.method == 'POST' and request.FILES['movimiento']:
            csv = pd.read_csv(file)
            for i in range(len(csv)):
                try:
                    # ESPERANDO LA DOCUMENTACION PARA SABER TODOS LOS CAMPOS
                    # QUE PIDE 'DATA'
                    Movimiento.objects.create(id_entidad=csv['id_entidad'][i],
                                              id_credito=csv['id_credito'][i],
                                              origen_pago=csv[
                                                'origen_pago'][i],
                                              tipo_cargo=csv['tipo_cargo'][i],
                                              tipo_cargo_e=csv[
                                                'tipo_cargo_e'][i],
                                              tipo_moneda=csv[
                                                'tipo_moneda'][i],
                                              monto_pago=csv['monto_pago'][i],
                                              fecha_pago=csv['fecha_pago'][i],
                                              payment_made_by=csv[
                                                'payment_made_by'][i]
                                              )
                    # ESPERANDO LA DOCUMENTACION PARA SABER TODOS LOS CAMPOS
                    # QUE PIDE 'DATA'
                    last = Movimiento.objects.last()
                    data = {'id_entidad': last.id_entidad,
                            'id_credito': last.id_credito,
                            'origen_pago': last.origen_pago,
                            'tipo_cargo': last.tipo_cargo,
                            'tipo_cargo_e': last.tipo_cargo_e,
                            'tipo_moneda': last.tipo_moneda,
                            'monto_pago': last.monto_pago,
                            'fecha_pago': last.fecha_pago,
                            'payment_made_by': last.payment_made_by
                            }
                    [cod, stat] = llamada(data)
                    last.status_code = stat
                    last.mensaje = cod
                    self.message_user(request, "{}".format(cod))
                    last.save()
                except Exception as e:
                    self.message_user(request, ("Error en la carga del \
                    movimiento con id_credito {} en la linea: {}".format(
                        csv['id_credito'][i], i)))
                    print(e)

    # SE MANTIENEN COMENTADOS POR SI SE USAN EN UN FUTURO.
    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     last = Movimiento.objects.last()
    #     data = {'id': form.cleaned_data['id_entidad'],
    #             'id_entidad': form.cleaned_data['id_entidad'],
    #             'id_credito': form.cleaned_data['id_credito'],
    #             'origen_pago': form.cleaned_data['origen_pago'],
    #             'tipo_cargo': form.cleaned_data['tipo_cargo'],
    #             'tipo_cargo_e': form.cleaned_data['tipo_cargo_e'],
    #             'tipo_moneda': form.cleaned_data['tipo_moneda'],
    #             'monto_pago': form.cleaned_data['monto_pago'],
    #             'fecha_pago': form.cleaned_data['fecha_pago'],
    #             'comentarios': form.cleaned_data['comentarios'],
    #             'cuenta': form.cleaned_data['cuenta'],
    #             'created_at': form.cleaned_data['created_at'],
    #             'payment_made_by': form.cleaned_data['payment_made_by'],
    #             'status': form.cleaned_data['status'],
    #             }
    #     [cod, txt] = llamada(data)
    #     last.respuesta = txt
    #     last.codigo = cod
    #     self.message_user(request, "TRANQUILA RAMIREZ, TRANQUILAA: " )
    #     last.save()


admin.site.register(Movimiento, MovimientoAdmin)
