import math

from django.http import HttpResponseForbidden
from django.utils import timezone
from django.contrib.auth.models import User

from graphene_django.views import GraphQLView
from graphql_jwt.shortcuts import get_user_by_token

from demograficos.models.profileChecks import InfoValidator as Validator
from demograficos.models import GeoLocation, GeoDevice, UserLocation
import logging

db_logger = logging.getLogger("db")

noToken_validate = [
    'tokenAuth',
    'unBlockAccount',
    'updateDevice',
    'blockAccountEmergency'
]

block_exception = [
    'unBlock',
    'updateDevice',
    'blockAccountEmergency',
]

uuid_exception = [
    'updateDevice',
    'recoverPassword',
    'blockAccountEmergency'
]


class LoggingGraphQLView(GraphQLView):
    def dispatch(self, request, *args, **kwargs):
        try:
            data = self.parse_body(request)
            query = data['query']
            try:
                token = str.encode(data['variables']['token'])
                user = get_user_by_token(token)
                username = user.username
            except Exception:
                if self.query_ex(query, noToken_validate):
                    username = (data['variables']['username'])
                    password = (data['variables']['password'])
                    user = User.objects.get(username=username)
                if not user.check_password(password):
                    return super().dispatch(request, *args, **kwargs)
        except Exception:
            return super().dispatch(request, *args, **kwargs)
        last_location = UserLocation.objects.filter(user=user).last()

        lat = request.headers.get("Location-Lat")
        lon = request.headers.get("Location-Lon")
        current_location = UserLocation.objects.create(user=user,
                                                       date=timezone.now())
        if lat and lon:
            location = GeoLocation.objects.create(lat=lat, lon=lon)
            current_location.location = location
            current_location.save()
            if last_location:
                # print(last_location.date)
                hours = (timezone.now() -
                         last_location.date).total_seconds()
                hours /= 3600
                # if request.headers.get("delta"):
                #     hours +=
                max_dist = self.get_max_distance(hours)
                dist = self.distance(last_location, current_location)
                if dist > max_dist + 100:
                    # Crear warning
                    pass
        device_id = request.headers.get("Device-Id")
        if device_id:
            device = GeoDevice.objects.create(uuid=device_id)
            current_location.device = device
            current_location.save()
            if username is not None:
                # valid_device = LoggingGraphQLView.set_screen(uuid=device_id,
                #    username=username)
                LoggingGraphQLView.set_screen(uuid=device_id,
                                              username=username)
                # if not valid_device and not self.query_ex(
                #     query, uuid_exception
                # ):
                #     return HttpResponseForbidden("UUID incorrecto")
        if user.Uprofile.status != 'O' and not self.query_ex(
                query, block_exception):
            return HttpResponseForbidden("action forbidden, user blocked")
        return super().dispatch(request, *args, **kwargs)

    @classmethod
    def set_screen(cls, uuid, username):
        try:
            user = User.objects.get(username=username)
            # device = user.udevices.get(activo=True)
            # if device.uuid != uuid:
            #     print('setting screen to emergency for user {}'.format(
            #         username))
            #     Validator.setComponentValidated(alias='dispositivo',
            #                                     user=user,
            #                                     valid=False,
            #                                     motivo='Este dispositivo es \
            #                                     diferente al que tenemos \
            #                                     registrado')
            #     return False
            # else:
            Validator.setComponentValidated(alias='dispositivo',
                                            user=user,
                                            valid=True,
                                            motivo='')
            return True
            # print('normal start for user {}'.format(username))
        except Exception as e:
            msg = "[Inicio de sesión] No se pudo obtener device activo en \
                Udevices.Error: {}.".format(e)
            db_logger.info(msg)
            pass
            # print('normal start for user {}'.format(username))

    @classmethod
    def distance(cls, last, current):
        """ Se debe calcular la distancia entre last y current, es decir.
            entre el punto de la actual petición y el punto donde se hizo
            la última petición. """

        r = 6.371 * (10 ** 6)
        cs = math.cos
        sn = math.sin
        def rad(f): return math.radians(float(f))
        try:
            latA = rad(last.location.lat)
            lonA = rad(last.location.lon)
            latB = rad(current.location.lat)
            lonB = rad(current.location.lon)
        except Exception:
            return 0
        A = (cs(latA)*cs(lonA), sn(latA), cs(latA)*sn(lonA))
        B = (cs(latB)*cs(lonB), sn(latB), cs(latB)*sn(lonB))
        dx = (A[0] - B[0])
        dy = (A[1] - B[1])
        dz = (A[2] - B[2])
        d = r * math.sqrt(dx * dx + dy * dy + dz * dz)
        # print((2 * r - d ** 2) / (2 * r))
        return (r * math.acos((2 * r*r - d ** 2) / (2 * r*r)))/1000

    @classmethod
    def get_max_distance(cls, hours):
        plane_vel = 1000  # km/h
        # Lo que recorre un avión en dos horas
        # se resta a las horas efectivas tiempo ascenso y descenso y esperas
        dist = plane_vel * (hours - max(0, 100/60))
        return dist

    @classmethod
    def query_ex(cls, query, list):
        if [x for x in list if x in query]:
            return True
        return False
