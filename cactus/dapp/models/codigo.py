from django.db import models


class CodigoCobro(models.Model):

    user = models.CharField(max_length=50, blank=False, null=False)
    code = models.TextField(max_length=500, blank=True, null=True)
    security = models.TextField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = 'Codigo de Cobro'
        verbose_name_plural = 'Codigos de Cobro'

    def __str__(self):
        return self.user
