from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class PdfLegal(models.Model):
    """
    ``Attributes:``
    nombre = CharField(max_length=69, blank=True)
    """
    nombre = models.CharField(max_length=69, blank=True)

    class Meta():
        verbose_name_plural = 'Clausulas Legales'

    def __str__(self):
        return self.nombre


class PdfLegalUser(models.Model):
    """
    ``Attributes:``
    nombre = CharField(max_length=69, blank=True)
    Pdf = FileField(upload_to='docs/pdfLegal', blank=True, null=True)
    fecha = DateTimeField(auto_now=True)
    validado = BooleanField(default=False)
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.ForeignKey(PdfLegal, on_delete=models.DO_NOTHING)
    Pdf = models.FileField(upload_to='docs/pdfLegal', blank=True, null=True)
    fecha = models.DateTimeField(auto_now=True)
    validado = models.BooleanField(default=False)

    class Meta():
        verbose_name_plural = 'Clausulas Legales de Usuario'

    def __str__(self):
        return self.nombre.nombre


@receiver(post_save, sender=PdfLegalUser)
def kitlegal(sender, instance, created, **kwargs):
    if created:
        user_ = User.objects.get(username=instance.user)
        uprofile = user_.Uprofile
        if instance.nombre.nombre == "comisiones":
            uprofile.kitComisiones = instance.Pdf
        elif instance.nombre.nombre == "terminos_y_condiciones":
            uprofile.kitTerminos = instance.Pdf
        elif instance.nombre.nombre == "aviso_de_privacidad":
            uprofile.kitPrivacidad = instance.Pdf
        elif instance.nombre.nombre == "declaraciones":
            uprofile.kitDeclaraciones = instance.Pdf
        uprofile.save()
