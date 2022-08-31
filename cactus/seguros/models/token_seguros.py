from django.db import models


class TokenSeguros(models.Model):
    segurotoken = models.CharField(max_length=200, blank=True, null=True)
