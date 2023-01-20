from django.db import models
from django.contrib.auth.models import User


class TransferenciasMensuales(models.Model):

    transferencias_mensuales = models.CharField(null=True,
                                                blank=True,
                                                max_length=50)
    codigo = models.CharField(null=True,
                              blank=True,
                              max_length=3)

    def __str__(self):
        return str(self.transferencias_mensuales)


class OperacionesMensual(models.Model):

    operaciones_mensuales = models.CharField(null=True,
                                             blank=True,
                                             max_length=50)
    codigo = models.CharField(null=True,
                              blank=True,
                              max_length=3)

    def __str__(self):
        return str(self.operaciones_mensuales)


class UsoCuenta(models.Model):

    uso_de_cuenta = models.CharField(null=True,
                                     blank=True,
                                     max_length=50)
    codigo = models.CharField(null=True,
                              blank=True,
                              max_length=3)

    def __str__(self):
        return str(self.uso_de_cuenta)


class OrigenDeposito(models.Model):

    origen = models.CharField(null=True,
                              blank=True,
                              max_length=50)
    codigo = models.CharField(null=True,
                              blank=True,
                              max_length=3)

    def __str__(self):
        return str(self.origen)


class PerfilTransaccionalDeclarado(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_perfil'
    )

    transferencias_mensuales = models.ForeignKey(
        TransferenciasMensuales,
        on_delete=models.CASCADE,
    )

    operaciones_mensuales = models.ForeignKey(
        OperacionesMensual,
        on_delete=models.CASCADE,
    )

    uso_cuenta = models.ForeignKey(
        UsoCuenta,
        on_delete=models.CASCADE,
    )

    origen = models.ForeignKey(
        OrigenDeposito,
        on_delete=models.CASCADE,
    )

    status = (
        ("Pendiente", "Pendiente"),
        ("Aprobado", "Aprobado"),
        ("Rechazado", "Rechazado")
    )

    status_perfil = models.CharField(null=True,
                                     blank=True,
                                     max_length=50,
                                     choices=status)

    def __str__(self):
        return str(self.user)
