from django.contrib import admin
from pld.models import Customer, Contrato, Movimiento, adminUtils
from pld.utils.customer import llamada1
import pandas as pd
from django.urls import path
from django.http import HttpResponseRedirect


class UserContratoInline(admin.TabularInline):
    model = Contrato
    verbose_name_plural = 'Contratos'


class UserPLDMovimientoInline(admin.TabularInline):
    model = Movimiento
    verbose_name_plural = 'Movimientos'


class CustomerAdmin(admin.ModelAdmin):
    change_list_template = "boton/customer.html"
    inlines = (UserContratoInline, UserPLDMovimientoInline,)
    list_display = ('id_entidad',
                    'tipo',
                    'nombre',
                    'actua_cuenta_propia',
                    'rfc',
                    'curp',
                    'status_code',
                    'mensaje',
                    'tienePLD',
                    )

    def has_add_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path('customer/', self.get_customer)]
        return my_urls + urls

    def get_customer(self, request):
        try:
            csv = request.FILES['customer']
        except Exception:
            self.message_user(request, "Asegurate de cargar un archivo")
            return HttpResponseRedirect("../")
        self.upload_customer(csv, request)
        return HttpResponseRedirect("../")

    def upload_customer(self, file, request):
        admin_Util = adminUtils.objects.get(id=1)
        if admin_Util.activo and request.method == 'POST' and request.FILES[
                'customer']:
            csv = pd.read_csv(file)
            for i in range(len(csv)):
                try:
                    # ESPERANDO LA DOCUMENTACION PARA SABER TODOS LOS CAMPOS
                    # QUE PIDE 'DATA'
                    Customer.objects.create(id_entidad=csv['id_entidad'][i],
                                            tipo=csv['tipo'][i],
                                            nombre=csv['nombre'][i],
                                            actua_cuenta_propia=csv[
                                                'actua_cuenta_propia'][i],
                                            rfc=csv['curp'][i][:10],
                                            curp=csv['curp'][i],
                                            apaterno=csv['apaterno'][i],
                                            amaterno=csv['amaterno'][i],
                                            )
                    # ESPERANDO LA DOCUMENTACION PARA SABER TODOS LOS CAMPOS
                    # QUE PIDE 'DATA'
                    last = Customer.objects.last()
                    data = {'id_entidad': last.id_entidad,
                            'tipo': last.tipo,
                            'nombre': last.nombre,
                            'actua_cuenta_propia': last.actua_cuenta_propia,
                            'rfc': last.rfc,
                            'curp': last.curp,
                            'apaterno': last.apaterno,
                            'amaterno': last.amaterno,
                            }
                    [bak, cod, stat] = llamada1(data)
                    aprobado = False
                    last.id_back = bak
                    last.status_code = stat
                    last.mensaje = cod
                    if stat == 200:
                        aprobado = True
                        last.tienePLD = aprobado
                    self.message_user(request, "{}".format(cod))
                    last.save()
                except Exception as e:
                    self.message_user(request, ("Hubo un error en la carga del \
                    customer con CURP {} en la linea: {}".format(
                        csv['curp'][i], i)))
                    print(e)

    # SE MANTIENEN COMENTADOS POR SI SE USAN EN UN FUTURO.
    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     last = Customer.objects.last()
    #     data = {#'id': form.cleaned_data['id'],  # Es el 'pk' del csv
    #             'id_entidad': form.cleaned_data['id_entidad'],
    #             'tipo': form.cleaned_data['tipo'],
    #             'actividad_empresarial': form.cleaned_data[
    #                 'actividad_empresarial'],
    #             'sector_economico': form.cleaned_data['sector_economico'],
    #             'apaterno': form.cleaned_data['apaterno'],
    #             'amaterno': form.cleaned_data['amaterno'],
    #             'nombre': form.cleaned_data['nombre'],
    #             'vinculado': form.cleaned_data['vinculado'],
    #             'actua_cuenta_propia': form.cleaned_data[
    #                 'actua_cuenta_propia'],
    #             'genero': form.cleaned_data['genero'],
    #             'rfc': form.cleaned_data['rfc'],
    #             'curp': form.cleaned_data['curp'],
    #             'fecha_nacimiento': form.cleaned_data['fecha_nacimiento'],
    #             'pais_nacimiento': form.cleaned_data['pais_nacimiento'],
    #             'nacionalidad': form.cleaned_data['nacionalidad'],
    #             'e_f_nacimiento': form.cleaned_data['e_f_nacimiento'],
    #             'telefono_fijo': form.cleaned_data['telefono_fijo'],
    #             'telefono_movil': form.cleaned_data['telefono_movil'],
    #             'correo_electronico': form.cleaned_data[
                    # 'correo_electronico'],
    #             'profesion': form.cleaned_data['profesion'],
    #             'actividad': form.cleaned_data['actividad'],
    #             'no_empleados': form.cleaned_data['no_empleados'],
    #             'actividad_cnbv': form.cleaned_data['actividad_cnbv'],
    #             'origen_ingresos': form.cleaned_data['origen_ingresos'],
    #             'or_pais': form.cleaned_data['or_pais'],
    #             'or_localidad': form.cleaned_data['or_localidad'],
    #             'dr_localidad': form.cleaned_data['dr_localidad'],
    #             'or_actividad': form.cleaned_data['or_actividad'],
    #             'fines_credito': form.cleaned_data['fines_credito'],
    #             'puesto_gobierno': form.cleaned_data['puesto_gobierno'],
    #             'descripcion_puesto': form.cleaned_data[
                    # 'descripcion_puesto'],
    #             'periodo_puesto': form.cleaned_data['periodo_puesto'],
    #             'calle': form.cleaned_data['calle'],
    #             'no_exterior': form.cleaned_data['no_exterior'],
    #             'no_interior': form.cleaned_data['no_interior'],
    #             'cp': form.cleaned_data['cp'],
    #             'colonia': form.cleaned_data['colonia'],
    #             'municipio': form.cleaned_data['municipio'],
    #             'ciudad': form.cleaned_data['ciudad'],
    #             'ef_domicilio': form.cleaned_data['ef_domicilio'],
    #             'estado_domicilio': form.cleaned_data['estado_domicilio'],
    #             'pais_domicilio': form.cleaned_data['pais_domicilio'],
    #             'fecha_proxima_revision': form.cleaned_data[
    #                 'fecha_proxima_revision'],
    #             'comentarios': form.cleaned_data['comentarios'],
    #             'status': form.cleaned_data['status'],
    #             'no_cliente': form.cleaned_data['no_cliente'],
    #             'created_at': form.cleaned_data['created_at'],
    #             'updated_at': form.cleaned_data['updated_at']
    #             }
    #
    #     [cod, txt] = llamada(data)
    #     last.respuesta = txt
    #     last.codigo = cod
    #     self.message_user(request, "{}".format(txt))
    #     last.save()


admin.site.register(Customer, CustomerAdmin)
