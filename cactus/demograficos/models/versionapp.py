from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver


class VersionApp(models.Model):
    version = models.CharField(max_length=2056)
    activa = models.BooleanField(default=True)
    url_android = models.URLField(blank=True, null=True)
    url_ios = models.URLField(blank=True, null=True)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.version


@receiver(pre_save, sender=VersionApp)
def desactiva_version(sender, instance, **kwargs):
    version = VersionApp.objects.filter(activa=True)

    if version.count() >= 2:
        version.filter(fecha=version.first().fecha).update(activa=False)
