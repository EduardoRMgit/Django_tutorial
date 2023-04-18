import graphene
import json
from base64 import b64encode
import requests
from demograficos.models.telefono import Telefono
from demograficos.models.direccion import Direccion
from ..methods import to_dict
from demograficos.models.userProfile import UserProfile
from django.contrib.auth import get_user_model
from ..models.transaccion import TransaccionDDE
from datetime import datetime, timedelta
from graphene_django.types import DjangoObjectType
from demograficos.schemas.userProfileSchema import UserProfileType
from demograficos.utils.tokendinamico import tokenD


class TransaccionDDEType(DjangoObjectType):
    class Meta:
        model = TransaccionDDE


class CreateDde(graphene.Mutation):
    confirmacion = graphene.String()
    id = graphene.String()
    telefono = graphene.String()
    direccion = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        token_d = graphene.String(required=True)
        local = graphene.Boolean()
        flag_tel = graphene.Boolean()
        flag_dir = graphene.Boolean()
        flag_user = graphene.Boolean()

    def mutate(self, info, token_d, token, local=False, flag_tel=False,
               flag_dir=False, flag_user=False):
        mutation_u = """
        mutation($username: String!, $up: String!,
                 $tel_dict: String!, $dir_dict: String!){
        createUser(username: $username, up: $up, utelefono: $tel_dict,
                   udireccion: $dir_dict){
            user{
                id
                }
            telefono
            direccion
        }
        }
        """

        user = info.context.user
        up = user.Uprofile
        dinamico = tokenD()

        if user.is_anonymous or not dinamico.verify(token_d):
            return None
        if not flag_tel and not up.validacion_telefono:
            raise Exception('telefono no validado')
        if not flag_user and not up.validacion_perfil:
            raise Exception('perfil no validado')
        if not flag_dir and not up.validacion_direccion:
            raise Exception('direccion no validada')
        url = 'https://dde.inguz.site/graphql' if not local else  \
              'http://127.0.0.1:8080/graphql'
        userAndPass = b64encode(b"test:t35t3r").decode("ascii")
        headers = {'Accept': 'application/json',
                   'Authorization': 'Basic %s' % userAndPass}
        up_dict = {
                'id_cactus': user.pk,
                'name': user.first_name,
                'apPaterno': user.last_name,
                'apMaterno': up.apMaterno if up.apMaterno else '',
                'ciudad_nacimiento': up.ciudad_nacimiento,  # noqa:E501
                'nacionalidad': up.nacionalidad,
                'correo': user.email,
                'sexo': up.sexo,
                'fechaNaciemiento': str(up.fecha_nacimiento) if \
                up.fecha_nacimiento else None,
                'numero_INE': up.numero_INE,
                'ocupacion': up.ocupacion,

                'curp': up.curp,
                'rfc': up.rfc,
                'cuentaClabe': up.cuentaClabe,
                }
        try:
            utelefono = Telefono.objects.filter(user=user, activo=True)[0]
        except Exception:
            if not flag_tel:
                raise Exception('usuario no tiene telefonos activos')
        try:
            udireccion = Direccion.objects.get(user=user, activo=True)
        except Exception:
            raise Exception('usuario no tiene direcciones activas')

        try:
            tel_dict = to_dict(utelefono)
            dir_dict = to_dict(udireccion)
        except Exception as e:
            raise Exception('profile serialization error', e)

        variables = {'username': user.username, 'up': json.dumps(up_dict),
                     'tel_dict': json.dumps(tel_dict),
                     'dir_dict': json.dumps(dir_dict)}

        data_u = {"query": mutation_u, "variables": json.dumps(variables)}

        try:
            r = requests.post(url=url, headers=headers, data=data_u)
        except Exception:
            raise Exception('connection failed')
        try:
            content = json.loads(r._content)
        except Exception:
            raise Exception('problem load dde response')
        if 'errors' in content:
            return Exception('dde error :' + content['errors'][0]['message'])
        response = r.json()['data']['createUser']
        r_id = response['user']['id']
        r_tel = response['telefono']
        r_direccion = response['direccion']
        up.id_dde = r_id
        up.confirmacion_dde = True
        up.save()
        return CreateDde(confirmacion='ok',
                         id=r_id, telefono=r_tel, direccion=r_direccion)


class AbonoLinea(graphene.Mutation):
    transaccion = graphene.Field(TransaccionDDEType)
    profile = graphene.Field(UserProfileType)

    class Arguments:
        id_dde = graphene.Int(required=True)
        id = graphene.Int(required=True)
        monto = graphene.String(required=True)

    def mutate(self, info, id_dde, id, monto):
        try:
            user = get_user_model().objects.get(pk=id)
        except Exception:
            raise Exception('user with id {} does not exist'.format(id))
        try:
            queryset = UserProfile.objects.filter(user=user, id_dde=id_dde)
            UserProfile.objects.get(user=user, id_dde=id_dde)
        except Exception as e:
            raise Exception(queryset, '{} {} {}'.format(id_dde, user.username,
                            e))
        try:
            monto = float(monto)
            fecha = (datetime.now() +
                     timedelta(hours=24)).strftime('transaccion%Y%m%d')
        except Exception as e:
            raise Exception('parse error', e)
        up = user.Uprofile
        if up.saldo_cuenta < monto:
            return Exception('saldo insuficiente')
        monto2F = "{:.2f}".format(monto)

        try:
            transaccion = TransaccionDDE.objects.create(
                user=user,
                monto=monto2F,
                fechaTrans=fecha,
                )
        except Exception as e:
            raise Exception('error user-transaccion {}'.format(id), e)
        return AbonoLinea(transaccion=transaccion, profile=up)


class Mutation(graphene.ObjectType):

    create_dde = CreateDde.Field()
    abono_linea = AbonoLinea.Field()
