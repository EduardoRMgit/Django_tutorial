from django.contrib import admin
from pld.models import Contrato, adminUtils
from pld.utils.contract import llamada2
from django.urls import path
import pandas as pd
from django.http import HttpResponseRedirect


class ContratoAdmin(admin.ModelAdmin):
    change_list_template = "boton/contrato.html"
    list_display = (
        'id_entidad',
        'curp',
        'rfc',
        'no_credito',
        'unidad_credito',
        'tipo_moneda',
        'T1',
        'T2',
        'T3',
        'instrumento_monetario',
        'canales_distribucion',
        'Estado',
        'status_code',
        'mensaje',
        'user',
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path('contrato/', self.get_contrato)]
        return my_urls + urls

    def get_contrato(self, request):
        try:
            csv = request.FILES['contrato']
        except Exception:
            self.message_user(request, "Asegurate de cargar un archivo")
            return HttpResponseRedirect("../")
        self.upload_contrato(csv, request)
        return HttpResponseRedirect("../")

    def upload_contrato(self, file, request):
        admin_Util = adminUtils.objects.get(id=1)
        if admin_Util.activo and request.method == 'POST' and request.FILES[
                'contrato']:
            csv = pd.read_csv(file)
            for i in range(len(csv)):
                try:
                    # ESPERANDO LA DOCUMENTACION PARA SABER TODOS LOS CAMPOS
                    # QUE PIDE 'DATA'
                    Contrato.objects.create(id_entidad=csv['id_entidad'][i],
                                            # rfc=csv['rfc'][i],
                                            curp=csv['curp'][i],
                                            no_credito=csv['no_credito'][i],
                                            unidad_credito=csv[
                                            'unidad_credito'][i],
                                            tipo_moneda=csv['tipo_moneda'][i],
                                            T1=csv['T1'][i],
                                            T2=csv['T2'][i],
                                            T3=csv['T3'][i],
                                            instrumento_monetario=csv[
                                                'instrumento_monetario'][i],
                                            canales_distribucion=csv[
                                                'canales_distribucion'][i],
                                            Estado=csv['Estado'][i]
                                            )
                    # ESPERANDO LA DOCUMENTACION PARA SABER TODOS LOS CAMPOS
                    # QUE PIDE 'DATA'
                    last = Contrato.objects.last()
                    data = {'id_entidad': last.id_entidad,
                            # 'rfc': last.rfc,
                            'curp': last.curp,
                            'no_credito': last.no_credito,
                            'unidad_credito': last.unidad_credito,
                            'tipo_moneda': last.tipo_moneda,
                            'T1': last.T1,
                            'T2': last.T2,
                            'T3': last.T3,
                            'instrumento_monetario':
                                last.instrumento_monetario,
                            'canales_distribucion': last.canales_distribucion,
                            'Estado': last.Estado
                            }
                    [cod, stat] = llamada2(data)
                    last.status_code = stat
                    last.mensaje = cod
                    self.message_user(request, "{}".format(cod))
                    last.save()
                except Exception as e:
                    self.message_user(request, ("Hubo un error en la carga del \
                    contrato con CURP {} en la linea: {}".format(
                        csv['curp'][i], i)))
                    print(e)

    # SE MANTIENEN COMENTADOS POR SI SE USAN EN UN FUTURO.
    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     last = Contrato.objects.last()
    #     data = {
    #             'id_entidad': form.cleaned_data['id_entidad'],
    #             'curp': form.cleaned_data['curp'],
    #             'rfc': form.cleaned_data['rfc'],
    #             'no_credito': form.cleaned_data['no_credito'],
    #             'unidad_credito': form.cleaned_data['unidad_credito'],
    #             'tipo_credito': form.cleaned_data['tipo_credito'],
    #             'tipo_moneda': form.cleaned_data['tipo_moneda'],
    #             'T1': form.cleaned_data['T1'],
    #             'T2': form.cleaned_data['T2'],
    #             'T3': form.cleaned_data['T3'],
    #             'T4': form.cleaned_data['T4'],
    #             'instrumento_monetario': form.cleaned_data[
    #                 'instrumento_monetario'],
    #             'canales_distribucion': form.cleaned_data[
                    # 'canales_distribucion'],
    #             'Estado': form.cleaned_data['Estado'],
    #             }
    #     [cod, txt] = llamada(data)
    #     last.respuesta = txt
    #     last.codigo = cod
    #     self.message_user(request, "QUE MUESTRAA, QUE MUESTRAAA: ")
    #     last.save()


admin.site.register(Contrato, ContratoAdmin)
