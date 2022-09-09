import requests
import json
# from pld.models.urls import UrlsPLD


def llamada1(data):
    # url = UrlsPLD.objects.filter(pk=2)[0]
    url = "https://gt-servicios.com/propld/customersapi/customer"
    headers = {
        'Accept': 'application/json',
        # 'X-API-KEY':'KYC-DSR92Sj2NgK8aPyPHXYSxjDs'
        'X-API-KEY': 'KYC-eWTR92Sj2NgK8aPyPHXYSxjVr'
    }

    # datos hardcoded basados en ejemplo
    data1 = {
        "id_entidad": 5500,
        "tipo": 1,
        "actividad_empresarial": 0,
        "sector_economico": 0,
        "apaterno": "Lopevfdvsdfvdfsvvdsfvsdfz",
        "amaterno": "cbjdkbcksnhnhhfdfbkjc",
        "nombre": "kjnsjhsfdbhsdgfb",
        "vinculado": 0,
        "actua_cuenta_propia": 1,
        "genero": "M",
        "rfc": "abcdefghi1234456789lknjhbsd",
        "curp": "abcdefghi1234456789lknjhbsd",
        "fecha_nacimiento": "1967-02-12",
        "pais_nacimiento": "MEXICO",
        "nacionalidad": "MEXICO",
        "e_f_nacimiento": "CIUDAD DE MEXICO",
        "telefono_fijo": "5512345678",
        "telefono_movil": "5512345678",
        "correo_electronico": "lcraul@gmail.com",
        "profesion": "INGENIERO",
        "actividad": "EMPLEADO PRIVADO",
        "no_empleados": 3,
        "actividad_cnbv": 8444098,
        "origen_ingresos": "",
        "or_pais": "MEXICO",
        "or_localidad": "CIUDAD DE MEXICO",
        "dr_localidad": "CIUDAD DE MEXICO",
        "or_actividad": "DE MI TRABAJO",
        "fines_credito": "COMPRAS",
        "puesto_gobierno": "NO ES PEP",
        "periodo_puesto": "",
        "calle": "LAUREL",
        "no_exterior": "30",
        "no_interior": "1-A",
        "cp": 3240,
        "colonia": "ALAMOS",
        "municipio": "BRNITO JUARE",
        "ciudad": "CIUDAD DE MEXICO",
        "ef_domicilio": "CIUDAD DE MEXICO",
        "estado_domicilio": "CIUDAD DE MEXICO",
        "pais_domicilio": "MEXICO",
        "fecha_proxima_revision": "2019-05-10",
        "status": 1,
        }

    r = requests.put(url, data=data1, headers=headers)
    k = json.loads(r.content)
    stat = r.status_code

    # Estos campos solo existen cuando se hace un registro exitoso
    # Cuando el registro falla, 'id' y 'message' no existen
    try:
        bak = k['id']
    except Exception as e:
        bak = '-1'
        print("e: ", e)
        print("bak:", bak)

    try:
        msg = k['message']
    except Exception as ex:
        msg = 'error en request'
        print("en la funcion llamada1(), msg: ", ex)

    return(bak, msg, stat)
