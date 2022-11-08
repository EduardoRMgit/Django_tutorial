from django.db import models


class Reembolso(models.Model):

    rc = models.IntegerField(default=0, blank=False, null=False)
    msg = models.CharField(max_length=60, blank=True, null=True)
    user = models.CharField(max_length=50, blank=True, null=True)
    data = models.TextField(max_length=1000, blank=True, null=True)
    security = models.TextField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = 'Reembolso'
        verbose_name_plural = 'Reembolsos'

    def __str__(self):
        return self.user
