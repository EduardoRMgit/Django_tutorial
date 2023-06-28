from banca.models import NivelCuenta
from django.contrib.auth.models import User
from datetime import datetime
from decimal import Decimal


class LimiteTrans(object):
    def __init__(self, id) -> None:
        """LimitesTrans

        Args:
            id (int): ID del usuario a evaluar.
            monto (float): Monto que está por transaccionarse.

        Raises:
            Exception para loggear errores al construir las variables.
        """
        try:
            self.user = User.objects.get(id=id)
            self.up = self.user.Uprofile
            self.nivel = NivelCuenta.objects.get(id=self.up.nivel_cuenta.id)
            self.today = datetime.now()
        except Exception as e:
            raise Exception(e)

    def trans_mes(self, monto):
        if self.nivel.trans_mes is None:
            return True
        trans = self.user.user_transaccion.filter(
            tipoTrans__medio="T",
            tipoTrans__tipo="R",
            fechaValor__year=self.today.year,
            fechaValor__month=self.today.month,
            statusTrans__nombre="exito"
        )
        total = sum([x.monto for x in trans]) + Decimal(monto)
        if not total <= self.nivel.trans_mes:
            return False
        return True

    def saldo_max(self, monto):
        if self.nivel.saldo_max is None:
            return True
        if not self.up.saldo_cuenta + monto <= self.nivel.saldo_max:
            return False
        return True

    def saldo_max_salida(self, monto):
        if self.nivel.saldo_max is None:
            return True
        trans = self.user.user_transaccion.filter(
            tipoTrans__medio="T",
            tipoTrans__tipo="E",
            fechaValor__year=self.today.year,
            fechaValor__month=self.today.month,
            statusTrans__nombre="exito",
        )
        total = sum([x.monto for x in trans]) + Decimal(monto)
        if not self.up.saldo_cuenta >= total <= self.nivel.saldo_max:
            return False
        return True

    def dep_efectivo_mes(self, monto):
        trans = self.user.user_transaccion.filter(
            tipoTrans__medio="E",
            tipoTrans__tipo="R",
            fechaValor__year=self.today.year,
            fechaValor__month=self.today.month,
            statusTrans__nombre__in=["exito", "esperando respuesta"]
        )
        total = sum([x.monto for x in trans]) + Decimal(monto)
        if not total <= self.nivel.dep_efectivo_mes:
            return False
        return True

    def dep_efectivo_dia(self, monto):
        trans = self.user.user_transaccion.filter(
            tipoTrans__medio="E",
            tipoTrans__tipo="R",
            fechaValor__year=self.today.year,
            fechaValor__month=self.today.month,
            fechaValor__day=self.today.day,
            statusTrans__nombre__in=["exito", "esperando respuesta"]
        )
        total = sum([x.monto for x in trans]) + Decimal(monto)
        if not total <= self.nivel.dep_efectivo_dia:
            return False
        return True

    def ret_efectivo_dia(self, monto):
        trans = self.user.user_transaccion.filter(
            tipoTrans__medio="E",
            tipoTrans__tipo="E",
            fechaValor__year=self.today.year,
            fechaValor__month=self.today.month,
            fechaValor__day=self.today.day,
            statusTrans__nombre__in=["exito", "esperando respuesta"]
        )
        total = monto
        for t in trans:
            if t.tipoTrans.codigo == "6":
                total += float(sum([x.scotiaRetiro.monto for x in trans]))
        if not total <= self.nivel.ret_efectivo_dia:
            return False
        return True
