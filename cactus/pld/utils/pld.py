import requests


url = 'https://gt-servicios.com/propld/customersapi/customer'
headers = {
        'Accept': 'application/json',
        # 'X-API-KEY':'KYC-DSR92Sj2NgK8aPyPHXYSxjDs'
        'X-API-KEY': 'KYC-eWTR92Sj2NgK8aPyPHXYSxjVr'
}

data = {
    'tipo': 1,
    'actividad_empresarial': 0,
    'sector_economico': 0,
    'apaterno': 'LOPEZ',
    'amaterno': 'SANCHEZ',
    'nombre': 'RAULL',
    'vinculado': 0,
    'actua_cuenta_propia': 1,
    'genero': 'M',
    'curp': 'LOCsdcsdc1vdfnjvfdnkdfvdfv',
    'fecha_nacimiento': '1967-02-12',
    'pais_nacimiento': 'MEXICO',
    'nacionalidad': 'MEXICO',
    'e_f_nacimiento': 'CIUDAD DE MEXICO',
    'telefono_movil': 5512345678,
    'profesion': 'INGENIERO',
    'actividad': 'EMPLEADO PRIVADO',
    'no_empleados': 0,
    'actividad_cnbv': 8944098,
    'origen_ingresos': 'SUELDOS',
    'or_pais': 'MEXICO',
    'or_localidad': 'CIUDAD DE MEXICO',
    'dr_localidad': 'CIUDAD DE MEXICO, ESTADOS UNIDOS',
    'or_actividad': 'DE MI TRABAJO',
    'fines_credito': 'COMPRAS',
    'puesto_gobierno': '',
    'descripcion_puesto': '',
    'periodo_puesto': '',
    'calle': 'LAUREL',
    'no_exterior': '30',
    'no_interior': '1-A',
    'cp': '03240',
    'colonia': 'ALAMOS',
    'municipio': 'BENITO JUAREZ',
    'ciudad': 'CIUDAD DE MEXICO',
    'ef_domicilio': 'CIUDAD DE MEXICO',
    'estado_domicilio': 'CIUDAD DE MEXICO',
    'pais_domicilio': 'MEXICO',
    'fecha_proxima_revision': '2019-05-10',
    'comentarios': 'CLIENTE PRO PRIMER VEZ PARA LA ENTIDAD'
                   'PLENAMENTE IDENTIFICADO Y VERIFICADO',
    'status': 1,
    'no_cliente': 'C2132342',
    'created_at': '2018-05-20',
    'updated_at': '2018-06-20'
}

r = requests.put(url, data=data, headers=headers)
print(r.content)
print(r.text)
print(r.request)
print(r.json)
