from django.db import models
from django.dispatch import receiver
from django.utils.safestring import mark_safe


class Logotypes(models.Model):
    """
    ``Attributes:``
    id_servicio =IntegerField(blank=True, null=True)
    Logo =ImageField(upload_to='servicios/logos/',
                             blank=True, null=True)

    """

    servicio = models.CharField(blank=True, null=True, max_length=20)
    id_servicio = models.IntegerField(blank=True, null=True)
    Logo = models.ImageField(upload_to='servicios/logos/',
                             blank=True, null=True)

    def Logotipo(self):
        if self.Logo:
            return mark_safe(
                '<img src="%s" style="width: 45px; height:45px;" />'
                % self.Logo.url)
        else:
            return 'No Image Found'
    Logotipo.short_description = 'Logo'

    class Meta():
        verbose_name_plural = 'Logotipos'

    def __str__(self):
        return str(self.id_servicio)


@receiver(models.signals.post_delete, sender=Logotypes)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Logotypes` object is deleted.
    """
    if instance.Logo:
        instance.Logo.delete()
