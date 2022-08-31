import logging
import decimal

from contabilidad.models import (ContableMovimiento, CuentaSaldo,
                                 TipoContableCuenta)


db_logger = logging.getLogger('db')


def balanza(transaccion, _tipo):
    tipo_de_movimiento = TipoContableCuenta.objects.get(id=_tipo)
    monto = float(decimal.Decimal(transaccion.monto))
    capacc = float(CuentaSaldo.objects.get(nombre='Scotia Propia').saldo)
    monto, capacc  # flake8

    orden = tipo_de_movimiento.cuentas.exclude(codigo='>->')
    orden = orden.filter(codigo__contains='-')
    orden = orden.order_by('orden')

    for cuenta in orden:
        regla_cargo = cuenta.regla.get(tipo=tipo_de_movimiento).regla_cargo
        cargo = decimal.Decimal(eval(regla_cargo))

        regla_abono = cuenta.regla.get(tipo=tipo_de_movimiento).regla_abono
        abono = decimal.Decimal(eval(regla_abono))

        if cuenta.movimientos.count() > 0:
            cuenta_saldo_inicial = cuenta.movimientos.last().saldo_final
        else:
            cuenta_saldo_inicial = decimal.Decimal(0)

        movimiento_data = {
            "saldo_inicial": cuenta_saldo_inicial,
            "cargo": cargo,
            "abono": abono,
            "saldo_final": cargo - abono,
            "cuenta": cuenta,
            "transaccion": transaccion,
            "tipo": tipo_de_movimiento
        }
        try:
            ContableMovimiento.objects.create(**movimiento_data)
        except Exception as ex:
            msg = "{}{}{}{}{}".format(
                repr(ex),
                "\nError al crear ContableMovimiento para transacción ",
                transaccion,
                "\nDatos del movimiento\n",
                movimiento_data
            )
            db_logger.error(msg)
            print(msg)

        print("cuenta", cuenta)
        # movimientos = ContableMovimiento.objects.filter(
        #     cuenta=cuenta,
        #     es_total=False,
        #     tipo=tipo_de_movimiento)
        # movimiento_total = ContableMovimiento.objects.get(
        #     cuenta=cuenta,
        #     es_total=True,
        #     tipo=tipo_de_movimiento
        # )

    #     movimiento_total.saldo_inicial = 0.00
    #     movimiento_total.cargo = sum(list(map(lambda c: c.cargo,
    #                                           movimientos)))
    #     movimiento_total.abono = sum(list(map(lambda c: c.abono,
    #                                           movimientos)))

    #     movimiento_total.saldo_final = (movimiento_total.cargo -
    #                                     movimiento_total.abono)
    #     movimiento_total.fecha = timezone.now()
    #     movimiento_total.save()

    # cuentas_total = ContableCuenta.objects.get(codigo='>->')
    # cuentas_total.cargo_actual = sum(list(map(lambda c: c.cargo_actual,
    #                                           orden)))
    # cuentas_total.abono_actual = sum(list(map(lambda c: c.abono_actual,
    #                                           orden)))
    # cuentas_total.saldo = sum(list(map(lambda c: c.saldo, orden)))
    # cuentas_total.save()
