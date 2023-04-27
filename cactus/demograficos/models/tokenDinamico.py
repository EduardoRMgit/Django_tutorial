from django.db import models
from demograficos.models import UserProfile
from django.utils import timezone


class TokenDinamico(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='user_tokenD')
    token = models.CharField(max_length=10)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user)
