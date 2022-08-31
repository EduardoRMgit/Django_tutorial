import decimal

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.utils import timezone

from banca.models.transaccion import Transaccion


class CuentaSaldo(models.Model):
    codigo = models.CharField(max_length=32, null=True, blank=True)
    nombre = models.CharField(max_length=64, null=True, blank=True)
    clabe = models.CharField(max_length=20, null=True, blank=True)
    saldo = models.DecimalField(
        max_digits=16, decimal_places=4, null=True, blank=True, default=0.00)

    class Meta:
        verbose_name_plural = "Saldo en cuentas"


class TipoContableCuenta(models.Model):
    tipo = models.CharField(max_length=64)
    activo = models.BooleanField(default=True)
    cuentas = models.ManyToManyField('ContableCuenta', through='CuentaTipo',
                                     related_name='tipos')

    def __str__(self):
        return self.tipo


class ContableCuenta(models.Model):
    codigo = models.CharField(max_length=32, null=True, blank=True)
    long_code = models.CharField(max_length=32, null=True, blank=True)
    orden = models.FloatField(null=True, blank=True)
    nombre = models.CharField(max_length=64, null=True, blank=True)
    sobrenombre = models.CharField(max_length=64, null=True, blank=True)
    cuenta_padre = models.ForeignKey('self',
                                     null=True,
                                     blank=True,
                                     on_delete=models.CASCADE,
                                     related_name='cuentas_hija')
    es_cuenta_totales = models.BooleanField(default=False)
    orden_admin = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Balanza General"

    def __str__(self):
        return self.codigo + '(' + self.nombre + ')'

    def __suma_asientos(self, movimientos, nombre):
        return sum(list(map(lambda m: m.__dict__.get(nombre), movimientos)))

    def __calcula_asiento(self, id_tipo, nombre_asiento):
        if self.es_cuenta_totales:
            suma_total = 0
            tipo_cuenta = TipoContableCuenta.objects.get(id=id_tipo)
            cuentas = tipo_cuenta.cuentas.filter(cuenta_padre__isnull=False)
            for cuenta in cuentas:
                suma_cuenta = self.__suma_asientos(
                    cuenta.movimientos.filter(tipo_id=id_tipo),
                    nombre_asiento)
                suma_total += suma_cuenta
            return suma_total

        cuentas = [self]
        if self.cuenta_padre is None:  # Es cuenta padre
            cuentas = self.cuentas_hija.all()

        total = decimal.Decimal(0)
        for c in cuentas:
            movimientos = c.movimientos.filter(tipo_id=id_tipo)
            total += self.__suma_asientos(movimientos, nombre_asiento)

        return total

    def calcula_saldo_inicial(self):
        es_cuenta_padre = self.cuenta_padre is None
        saldo_inicial = decimal.Decimal(0)
        return es_cuenta_padre, saldo_inicial

    def calcula_cargo(self, id_tipo):
        es_cuenta_padre = self.cuenta_padre is None
        cargo = self.__calcula_asiento(id_tipo, 'cargo')
        return es_cuenta_padre, cargo

    def calcula_abono(self, id_tipo):
        es_cuenta_padre = self.cuenta_padre is None
        abono = self.__calcula_asiento(id_tipo, 'abono')
        return es_cuenta_padre, abono

    def calcula_saldo_final(self, id_tipo):
        es_cuenta_padre = self.cuenta_padre is None
        saldo_final = self.__calcula_asiento(id_tipo, 'saldo_final')
        return es_cuenta_padre, saldo_final

    def actualiza_saldo(self, cargo, abono):
        if self.codigo in ['1102-0001', '3100-0001']:
            if self.codigo == '3100-0001':  # CAPACC
                banco = ContableCuenta.objects.get(codigo='1102-0001')
                if banco.movimientos.last().saldo_inicial == decimal.Decimal(
                        float('0.00')):
                    self.saldo = (banco.saldo - 500) * (-1)
                    self.save()
            if self.codigo == '1102-0001':  # BANCO
                self.saldo = self.saldo + (cargo - abono)
                self.save()

                scotia_propia = CuentaSaldo.objects.get(nombre='Scotia Propia')
                scotia_propia.saldo = self.saldo
                scotia_propia.save()
        elif self.codigo == '>->':
            return
        else:
            self.saldo = self.saldo + (cargo - abono)
            self.save()


class CuentaTipo(models.Model):
    cuenta = models.ForeignKey(
        ContableCuenta,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='regla'
    )
    tipo = models.ForeignKey(
        TipoContableCuenta,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='regla'
    )
    regla_cargo = models.CharField(max_length=128, null=True, blank=True)
    regla_abono = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return "{} - ({})".format(str(self.cuenta), str(self.tipo))


class ContableMovimiento(models.Model):
    saldo_inicial = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True, default=0.00)
    cargo = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True, default=0.00)
    abono = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True, default=0.00)
    saldo_final = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True, default=0.00)
    fecha = models.DateTimeField(
        default=timezone.now, null=True, blank=True)
    cuenta = models.ForeignKey(
        ContableCuenta,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="movimientos"
    )
    transaccion = models.ForeignKey(
        Transaccion,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="transacciones"
    )
    tipo = models.ForeignKey(
        TipoContableCuenta,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="movimientos"
    )

    class Meta:
        verbose_name_plural = "Movimientos"

    def __str__(self):
        return self.cuenta.codigo


@receiver(post_save, sender=CuentaSaldo)
def first_time_balance(sender, instance, created,  **kwargs):
    from .cuenta_contable import ContableCuenta
    banco = ContableCuenta.objects.get(codigo='1102-0001')
    sponsor = ContableCuenta.objects.get(codigo='2100-0001')
    # capacc = ContableCuenta.objects.get(codigo='3100-0001')

    banco.abono_actual = instance.saldo
    banco.saldo = instance.saldo + 500
    banco.save()

    sponsor.abono_actual = 500
    sponsor.saldo = 500 * (-1)
    sponsor.save()

    # if capacc.movimientos.count() == 2:
    #     capacc.abono_actual = instance.saldo
    #     capacc.saldo = instance.saldo * (-1)
    #     capacc.save()
