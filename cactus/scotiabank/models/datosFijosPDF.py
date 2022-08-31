from django.db import models


class DatosFijosPDF(models.Model):

    class Meta:
        verbose_name = "Datos fijos en comprobante"
        verbose_name_plural = "Datos fijos en comprobantes"

    TIPOS = (
        ('Retiro', 'Retiro Scotiabank'),
        ('Deposito', 'Depósito Scotiabank'),
    )

    tipo_transaccion = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        choices=TIPOS,
        verbose_name='Tipo de transacción',
        default="Retiro",
        unique=True
    )

    nombre_empresa = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Nombre del banco'
    )

    numero_empresa = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Número de empresa/convenio:'
    )

    instrucciones = models.TextField(max_length=500)

    def __str__(self):
        return str(self.tipo_transaccion)
