from django.db import models
from .instituciones import Institucion
from django.contrib.auth.models import User


class Prospectos(models.Model):
    """Potential customers

    ``Attributes:``

        - referencia(Char): ???

        - tarjeta(Char): card number.

        - telefono(Char): phone number.

        - vecesDeContacto(Integer): times being contacted.

        - candidato(Boolean): ???

        - sumaTotal(Float): ???

        - promedio(Float): ????

        - limiteCreditoReal(Float): ???

        - limiteCreditoRedondeado(Float): ???

        - maximo(Float): ???

        - minimo(Float): ???

        - desvEst(Float): ????

        - porcentaje(Float): ????

        - depositosPromedio(Float): Average deposits made by the \
            pontential customer.

        - fechaCreacion(DateTime): date and time of creation.

        - formato(Foreign): many to one field to the Institucion model.

        - user(OneToOne): one to one field to the django standard user model.

    """
    referencia = models.CharField(max_length=80)
    tarjeta = models.CharField(max_length=16)
    telefono = models.CharField(max_length=20, null=True)
    vecesDeContacto = models.IntegerField(default=0)
    candidato = models.BooleanField(default=False)
    sumaTotal = models.FloatField(default=0)
    promedio = models.FloatField(default=0)
    limiteCreditoReal = models.FloatField(default=0)
    limiteCreditoRedondeado = models.FloatField(default=0)
    maximo = models.FloatField(default=0)
    minimo = models.FloatField(default=0)
    desvEst = models.FloatField(default=0, null=True, blank=True)
    porcentaje = models.FloatField(default=10)
    depositosPromedio = models.FloatField(default=0)
    fechaCreacion = models.DateTimeField(auto_now=True)
    formato = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='Uprospecto')

    class Meta:
        verbose_name = 'Prospecto'
        verbose_name_plural = 'Prospectos'

    def __str__(self):
        return self.referencia


class Depositos(models.Model):
    """Deposits made

    ``Attributes:``

        - identificador(int): ???

        - fecha(date): date of the deposit.

        - importe(float): amount of the deposit.

        - prospecto(foreign): many to one to the Prospectos model.
    """
    identificador = models.IntegerField(default=1)
    fecha = models.DateField()
    importe = models.FloatField()
    prospecto = models.ForeignKey(Prospectos, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Deposito'
        verbose_name_plural = 'Depositos'
