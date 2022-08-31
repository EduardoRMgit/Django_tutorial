from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from demograficos.models import Fecha


@receiver(post_save, sender=User)
def populate_model_fecha(sender, instance, created, **kwargs):
    if created:
        fecha = Fecha.objects.create(user=instance)
        fecha.set_created()
        fecha.save()


@receiver(user_logged_in)
def create_fecha_user(sender, user, request, **kwargs):
    try:
        fecha = user.Ufecha.set_created()
    except Exception as e:
        print(e)
        fecha = Fecha.objects.create(user=user)
        fecha.set_created()
        fecha.save()
