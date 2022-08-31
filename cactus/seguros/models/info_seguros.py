from django.db import models
from django.contrib.auth.models import User


class InfoSeguros(models.Model):

    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='userinfoseguros'
    )

    num_poliza = models.CharField(max_length=200, blank=True, null=True)
