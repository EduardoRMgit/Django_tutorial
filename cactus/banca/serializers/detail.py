from rest_framework import serializers
from spei.models import StpTransaction


class DetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = StpTransaction
        fields = [
            'stpId',
            'fechaOperacion',
            'institucionOrdenante',
            'institucionBeneficiaria',
            'claveRastreo',
            'monto',
            'nombreOrdenante',
            'tipoCuentaOrdenante',
            'cuentaOrdenante',
            'rfcCurpOrdenante',
            'nombreBeneficiario',
            'tipoCuentaBeneficiario',
            'cuentaBeneficiario',
            'rfcCurpBeneficiario',
            'conceptoPago',
            'referenciaNumerica',
            'empresa',
            'tipoPago',
            'tsLiquidacion',
            'folioCodi'
        ]


class EstadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = StpTransaction
        fields = ['id',
                  'stpId',
                  'empresa',
                  'folioOrigen',
                  'estado',
                  'causaDevolucion',
                  'tsLiquidacion'
                  ]
