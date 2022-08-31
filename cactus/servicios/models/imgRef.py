from django.db import models
from django.dispatch import receiver
from django.utils.safestring import mark_safe


class ImgRef(models.Model):
    """
    ``Attributes:``
    id_servicio =IntegerField(blank=True, null=True)
    Imagenes_referencia =ImageField(upload_to='servicios/referencia/',
                                            blank=True, null=True)

    """
    servicio = models.CharField(blank=True, null=True, max_length=20)
    id_servicio = models.IntegerField(blank=True, null=True)
    Imagenes_referencia = models.ImageField(upload_to='servicios/referencia/',
                                            blank=True, null=True)

    def Imagen_Ayuda(self):
        if self.Imagenes_referencia:
            return mark_safe(
                '<img src="%s" style="width: 45px; height:45px;"/>'
                % self.Imagenes_referencia.url)
    Imagen_Ayuda.short_description = 'Imagen_Ayuda'

    class Meta():
        verbose_name_plural = 'Imagenes de Referencia'

    def __str__(self):
        return str(self.id_servicio)


@receiver(models.signals.post_delete, sender=ImgRef)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `ImgRef` object is deleted.
    """
    if instance.Imagenes_referencia:
        instance.Imagenes_referencia.delete()
