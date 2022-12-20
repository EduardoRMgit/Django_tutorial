from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
import random


class GeoLocation(models.Model):

    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return '{}, {}'.format(self.lat, self.lon)


class UDevice(models.Model):
    uuid = models.CharField(max_length=50, blank=False, default=None)
    activo = models.BooleanField(default=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='udevices',
        null=True
    )

    def __str__(self):
        return 'uudi: {}, username: {}, activo: {}'.format(self.uuid,
                                                           self.user.username,
                                                           self.activo)

    @classmethod
    def register(cls, uuid, user):
        device, created = UDevice.objects.get_or_create(uuid=uuid, activo=True)
        if not created:
            other = device.user
            if other is not user and not other.is_active:
                device.activo = False
                device = UDevice.objects.create(uuid=uuid, user=user)
            return
        device.user = user
        device.save()

    @classmethod
    def emulate_device(cls, user, uuid=None):
        if not uuid:
            uuid = random.randint(0, 1000)
        try:
            return cls.objects.create(user=user, uuid=uuid)
        except Exception as e:
            raise Exception(e)


class GeoDevice(models.Model):

    uuid = models.CharField(max_length=50)
    username = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.uuid


class UserLocation(models.Model):

    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='location'
    )
    location = models.ForeignKey(
        GeoLocation,
        null=True,
        on_delete=models.CASCADE,
        related_name='user_location'
    )
    device = models.ForeignKey(
        GeoDevice,
        null=True,
        on_delete=models.CASCADE,
        related_name='user_device'
    )
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} {} {}".format(self.user,
                                 self.device,
                                 self.location)
