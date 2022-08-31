import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
import requests
import json
import os
from seguros.models.info_seguros import InfoSeguros
from demograficos.models.userProfile import UserProfile
from demograficos.models.direccion import Direccion
from demograficos.models.telefono import Telefono


class InfoSegurosType(DjangoObjectType):
    class Meta:
        model = InfoSeguros


class UprofileType(DjangoObjectType):
    class Meta:
        model = UserProfile


class DireccionSegurosType(DjangoObjectType):
    class Meta:
        model = Direccion


class TelefonoSegurosType(DjangoObjectType):
    class Meta:
        model = Telefono


class AsignarSeguro(graphene.Mutation):
    response = graphene.String()

    class Arguments:
        token = graphene.String(required=True)

    @login_required
    def mutate(self, info, token):
        user = info.context.user

        if user is not None:

            site = os.getenv("SITE", "local")
            if site == "local":

                url = 'http://127.0.0.1:8080/graphql/'
            else:
                url = 'https://staging.zygoo.mx/graphql/'

        # TODO hacer entidad en seguroscactus que cree los usuarios
        # query = """ mutation($username: String!, $password: String!){
        #   tokenAuth(username:$username, password: $password){
        #     token
        #   }
        # }
        # """
        #
        # username = "alan"
        # password = "1234567890"
        #
        # variables = {"username": "{}".format(username),
        #              "password": "{}".format(password)}
        # vars = json.dumps(variables)
        # data = {"query": query, "variables": vars}
        # header = {'Accept': 'application/json'}
        #
        # r = requests.post(url, data=data, headers=header)
        # print(r.text)
        # token = json.loads(r.text)["data"]["tokenAuth"]["token"]
        #
        # print(token)

            uprofile = user.Uprofile
            username = user.username
            name = user.first_name
            lastNameP = user.last_name
            lastNameM = uprofile.apMaterno
            city = uprofile.ciudad_nacimiento
            nationality = uprofile.nacionalidad
            correo = user.email
            gender = uprofile.sexo
            # birthDate = UProfile.fechaNaciemiento
            numeroINE = uprofile.numero_INE
            occupation = uprofile.ocupacion
            curp = uprofile.curp
            rfc = uprofile.rfc
            # Direccion
            try:
                udireccion = Direccion.objects.get(user=user, activo=True)
                for key, value in udireccion.__dict__.items():
                    if value is None:
                        raise ValueError(key + " does not have value")

            except Direccion.DoesNotExist:
                raise Exception("User must have direccion")

            # udireccion = Direccion.objects.get(user=user)
            linea1 = udireccion.linea1
            linea2 = udireccion.linea2
            num_int = udireccion.num_int
            num_ext = udireccion.num_ext
            codPostal = udireccion.codPostal
            colonia = udireccion.colonia
            ciudad = udireccion.ciudad
            delegMunicipio = udireccion.delegMunicipio
            fechaCreacion_dir = str(udireccion.fechaCreacion)
            telefono_dir = udireccion.telefono
            activo_dir = udireccion.activo
            validado_dir = udireccion.validado
            country_dir = udireccion.country
            tipo_direccion = udireccion.tipo_direccion
            entidadFed = udireccion.entidadFed
            # telefono
            try:
                utelefono = Telefono.objects.get(user=user, activo=True)
                for key, value in utelefono.__dict__.items():
                    if value is None:
                        print(key)
                        raise ValueError(key + " does not have value")

            except Telefono.DoesNotExist:
                raise Exception("User must have telefono")

            # utelefono = Telefono.objects.get(user=user)
            telefono = utelefono.telefono
            extension = utelefono.extension
            fechaCreacion_tel = str(udireccion.fechaCreacion)
            country_tel = utelefono.country
            prefijo = utelefono.prefijo
            activo_tel = utelefono.activo
            validado_tel = utelefono.validado
            proveedorTelefonico = utelefono.proveedorTelefonico
            tipoTelefono = utelefono.tipoTelefono

            query = """
            mutation($username: String!, $name: String!, $lastNameP: String!,
                     $lastNameM: String!, $city: String!,
                     $nationality: String!, $correo: String!,
                     $gender: String!, $numeroINE: String!,
                     $occupation: String!, $curp: String!,
                     $rfc: String!,
                     $linea1: String!, $linea2: String!, $numInt: String!,
                     $numExt: String!, $codPostal: String!, $colonia: String!,
                     $ciudad: String!, $delegMunicipio: String!,
                     $fechaCreacionDir: String!, $telefonoDir: String!,
                     $activoDir: Boolean!, $validadoDir: Boolean!,
                     $countryDir: String!, $tipoDireccion: String!,
                     $entidadFed: String!,
                     $telefono: String!,
                     $extension: String!, $fechaCreacionTel: String!,
                     $countryTel: String!, $prefijo: String!,
                     $activoTel: Boolean!, $validadoTel: Boolean!,
                     $proveedorTelefonico: String!, $tipoTelefono: String!,
                     ){
              createUser(username: $username, name: $name,
                         lastNameP: $lastNameP,
                         lastNameM: $lastNameM, city: $city,
                         nationality: $nationality, correo: $correo,
                         gender: $gender, numeroIne: $numeroINE,
                         occupation: $occupation, curp: $curp, rfc: $rfc,
                         linea1: $linea1, linea2: $linea2, numInt: $numInt,
                         numExt: $numExt, codPostal: $codPostal,
                         colonia: $colonia, ciudad: $ciudad,
                         delegMunicipio: $delegMunicipio,
                         fechaCreacionDir: $fechaCreacionDir,
                         telefonoDir: $telefonoDir, activoDir: $activoDir,
                         validadoDir: $validadoDir,
                         countryDir: $countryDir,
                         tipoDireccion: $tipoDireccion,
                         entidadFed: $entidadFed,
                         telefono: $telefono,
                         extension: $extension,
                         fechaCreacionTel: $fechaCreacionTel,
                         countryTel: $countryTel, prefijo: $prefijo,
                         activoTel: $activoTel, validadoTel: $validadoTel,
                         proveedorTelefonico: $proveedorTelefonico,
                         tipoTelefono: $tipoTelefono,
                          ){
                user{
                  id
                  username
                  email
                  Uprofile{
                    numPoliza
                  }
                }
              }
            }
            """

            variables1 = {"username": "{}".format(username),
                          "name": "{}".format(name),
                          "lastNameP": "{}".format(lastNameP),
                          "lastNameM": "{}".format(lastNameM),
                          "city": "{}".format(city),
                          "nationality": "{}".format(nationality),
                          "correo": "{}".format(correo),
                          "gender": "{}".format(gender),
                          "numeroINE": "{}".format(numeroINE),
                          "occupation": "{}".format(occupation),
                          "curp": "{}".format(curp),
                          "rfc": "{}".format(rfc),
                          # direccion
                          "linea1": "{}".format(linea1),
                          "linea2": "{}".format(linea2),
                          "numInt": "{}".format(num_int),
                          "numExt": "{}".format(num_ext),
                          "codPostal": "{}".format(codPostal),
                          "colonia": "{}".format(colonia),
                          "ciudad": "{}".format(ciudad),
                          "delegMunicipio": "{}".format(delegMunicipio),
                          "fechaCreacionDir": "{}".format(fechaCreacion_dir),
                          "telefonoDir": "{}".format(telefono_dir),
                          "activoDir": activo_dir,
                          "validadoDir": validado_dir,
                          "countryDir": "{}".format(country_dir),
                          "tipoDireccion": "{}".format(tipo_direccion),
                          "entidadFed": "{}".format(entidadFed),
                          # telefono
                          "telefono": "{}".format(telefono),
                          "extension": "{}".format(extension),
                          "fechaCreacionTel": "{}".format(fechaCreacion_tel),
                          "countryTel": "{}".format(country_tel),
                          "prefijo": "{}".format(prefijo),
                          "activoTel": activo_tel,
                          "validadoTel": validado_tel,
                          "proveedorTelefonico": "{}".format(proveedorTelefonico),   # noqa:E501
                          "tipoTelefono": "{}".format(tipoTelefono),
                          }

            vars1 = json.dumps(variables1)
            data1 = {"query": query, "variables": vars1}
            header = {'Accept': 'application/json'}
            uprofile.con_seguro = True
            uprofile.save()
            s = requests.post(url, data=data1, headers=header)
            resp_json = json.loads(s.content)
            d = resp_json['data']['createUser']['user']['Uprofile']['numPoliza']   # noqa:E501
            InfoSeguros.objects.create(user=user, num_poliza=d)
            return AsignarSeguro(response=s.text)


class Mutation(graphene.ObjectType):
    asignar_seguro = AsignarSeguro.Field()
