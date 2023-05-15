import os
import boto3
import graphene

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType
from decimal import Decimal

from spei.stpTools import randomString
from spei.models import InstitutionBanjico

from banca.schemas.transaccionSchema import TransaccionType
from banca.models import (StatusTrans, TipoTransaccion,
                          Transaccion, SaldoReservado)
from banca.utils.limiteTrans import LimiteTrans

from scotiabank.utility.utcToLocal import utc_to_local
from scotiabank.utility.LineaCaptura import genera_linea_de_captura
from scotiabank.utility.ScotiaUtil import genera_pdf
from scotiabank.models import (ScotiaTransferencia,
                               ScotiaRetiro,
                               ScotiaDeposito,
                               DatosFijosPDF)

from demograficos.models.userProfile import UserProfile


def upload_s3(nombre_archivo, archivo):
    from cactus.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    directory = 'Comprobante'
    file_path = os.path.join(
        directory,
        nombre_archivo
    )
    file_path = os.path.join('docs/', file_path)
    client = boto3.client(
        's3',
        config=boto3.session.Config(signature_version='s3v4'),
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="us-east-2")
    client.upload_fileobj(archivo, "scotia-reportes", file_path)
    file_url = client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': "scotia-reportes",
            'Key': file_path
        },
        ExpiresIn=1440,
        HttpMethod=None)
    return file_url


class ScotiaTransferenciaType(DjangoObjectType):
    class Meta:
        model = ScotiaTransferencia


class ScotiaRetiroType(DjangoObjectType):
    class Meta:
        model = ScotiaRetiro


class ScotiaDepositoType(DjangoObjectType):
    class Meta:
        model = ScotiaDeposito


class UserUType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class Query(graphene.ObjectType):
    url_comprobante = graphene.List(TransaccionType,
                                    token=graphene.String(required=True),
                                    id_transaccion=graphene.Int(required=True))
    """
    Data:
    {
    urlComprobante(token: "", idTransaccion: 14)
    {scotiaretiro{urlComprobante}, scotiadeposito{urlComprobante}}
    }
    """

    def resolve_url_comprobante(self, info, **kwargs):
        id = kwargs.get("id_transaccion")
        deposito = ScotiaDeposito.objects.filter(transaccion=id)
        depo = deposito.count()
        retiro = ScotiaRetiro.objects.filter(transaccion=id)
        reti = retiro.count()
        if depo != 0:
            datos = DatosFijosPDF.objects.get(tipo_transaccion="Deposito")
            deposito = ScotiaDeposito.objects.get(transaccion=id)
            archivo, nombre_archivo = genera_pdf(deposito, datos)
            if settings.USE_S3:
                url = upload_s3(nombre_archivo, archivo)
            else:
                with open(nombre_archivo, 'wb') as f:
                    f.write(archivo.getbuffer())
                    deposito.comprobante_pdf.save(nombre_archivo, archivo)
                    url = deposito.comprobante_pdf.url
            deposito.url_comprobante = url
            deposito.save()
            return Transaccion.objects.filter(id=id)
        elif reti != 0:
            datos = DatosFijosPDF.objects.get(tipo_transaccion="Retiro")
            retiro = ScotiaRetiro.objects.get(transaccion=id)
            archivo, nombre_archivo = genera_pdf(retiro, datos)
            if settings.USE_S3:
                url = upload_s3(nombre_archivo, archivo)
            else:
                with open(nombre_archivo, 'wb') as f:
                    f.write(archivo.getbuffer())
                    retiro.comprobante_pdf.save(nombre_archivo, archivo)
                    url = retiro.comprobante_pdf.url
            retiro.url_comprobante = url
            retiro.save()
            return Transaccion.objects.filter(id=id)
        else:
            raise Exception("Transaccion invalida")


class CreateTransferenciaScotia(graphene.Mutation):
    """
    DATA:
        mutation {
          createScotiaTransferencia(
              token: {token},
              claveBeneficiario: "234234234",
              cuentaBeneficiario: "323232323",
              concepto: "aaaaaaa",
              institucionBeneficiariaInt: "04",
              monto: 20.2, nombreBeneficiario: "Paco",
              tipoCuentaBeneficiario: "03",
              rfcCurpBeneficiario: " ",
              ubicacion: "") {
            scotiaTransferencia{
              id
              fechaOperacion
              statusTrans
            }
          }
        }

    RESPONSE:
        {
          "data": {
            "createScotiaTransferencia": {
              "scotiaTransferencia": {
                "id": "6",
                "fechaOperacion": "2022-05-27T17:53:15.863711+00:00",
                "statusTrans": "A_0"
              }
            }
          }
        }
    """

    scotia_transferencia = graphene.Field(ScotiaTransferenciaType)
    user = graphene.Field(UserUType)

    class Arguments:
        token = graphene.String(required=True)
        institucionBeneficiariaInt = graphene.ID(required=True)
        monto = graphene.Float(required=True)
        nombreBeneficiario = graphene.String(required=True)
        tipoCuentaBeneficiario = graphene.String()
        cuentaBeneficiario = graphene.String(required=True)
        rfcCurpBeneficiario = graphene.String()
        clave_beneficiario = graphene.String(required=True)
        concepto = graphene.String(required=True)
        nip = graphene.String()
        ubicacion = graphene.String()

    @login_required
    def mutate(self, info,
               token,
               institucionBeneficiariaInt,
               monto,
               nombreBeneficiario,
               cuentaBeneficiario,
               clave_beneficiario,
               concepto,
               ubicacion,
               nip,
               tipoCuentaBeneficiario=None,
               rfcCurpBeneficiario=None):
        try:
            ordenante = info.context.user
        except Exception:
            raise Exception('Usuario inexistente')
        if UserProfile.objects.filter(user=ordenante).count() == 0:
            raise Exception('Usuario sin perfil')
        if ordenante.Uprofile.password:
            if not ordenante.Uprofile.check_password(nip):
                raise Exception('Nip esta mal')
        if monto == 0 or monto is None:
            raise Exception('Ingrese un monto válido')
        try:
            institucionBeneficiariaInt = (
                InstitutionBanjico.objects.get(id=institucionBeneficiariaInt))
        except Exception:
            raise Exception("Institucion no valida")
        comision = 4.00
        fecha = utc_to_local(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')
        claveR = randomString()
        status = StatusTrans.objects.get(nombre="esperando respuesta")
        tipo = TipoTransaccion.objects.get(codigo=16)
        main_trans = Transaccion.objects.create(
            user=ordenante,
            fechaValor=fecha,
            monto=float(comision),  # Revisar si incluye comisión
            statusTrans=status,
            tipoTrans=tipo,
            concepto=concepto,
            claveRastreo=claveR
        )

        scotia_transferencia = ScotiaTransferencia.objects.create(
            transaccion=main_trans,
            institucionBeneficiariaInt=institucionBeneficiariaInt,
            monto=monto,
            ordenante=ordenante,
            nombreBeneficiario=nombreBeneficiario,
            tipoCuentaBeneficiario=tipoCuentaBeneficiario,
            cuentaBeneficiario=cuentaBeneficiario,
            rfcCurpBeneficiario=rfcCurpBeneficiario,
            clave_beneficiario=clave_beneficiario,
            conceptoPago=concepto
        )

        return CreateTransferenciaScotia(
            scotia_transferencia=scotia_transferencia,
            user=ordenante
        )


class CreateRetiroScotia(graphene.Mutation):

    """
    DATA:
        mutation {
          createScotiaRetiro(
              token: {token},
              monto: 200.50,
              ubicacion: "aaaa") {
            scotiaRetiro {
              id
              fechaOperacion
              statusTrans
              tipoCuentaOrdenante
              claveRetiro
              comision
            }
          }
        }

    RESPONSE:
        {
        "data": {
            "createScotiaRetiro": {
            "scotiaRetiro": {
                "id": "2",
                "fechaOperacion": "2022-06-20T02:14:42.655424+00:00",
                "statusTrans": "A_0",
                "tipoCuentaOrdenante": "A_9",
                "claveRetiro": "646181974",
                "comision": 24.68
            }
            }
        }
        }
    """

    scotia_retiro = graphene.Field(ScotiaRetiroType)
    user = graphene.Field(UserUType)

    class Arguments:
        token = graphene.String(required=True)
        monto = graphene.Float(required=True)
        nip = graphene.String()
        ubicacion = graphene.String()

    @login_required
    def mutate(self, info,
               token,
               monto,
               ubicacion,
               nip):

        def _valida(expr, msg):
            if expr:
                raise Exception(msg)

        try:
            user = info.context.user
        except Exception:
            raise Exception('Usuario inexistente')

        monto = round(float(monto), 2)
        comision = 24
        saldo_inicial_usuario = user.Uprofile.saldo_cuenta

        _valida(UserProfile.objects.filter(user=user).count() == 0,
                'Usuario sin perfil')
        _valida(user.Uprofile.password is None,
                'El usuario no ha establecido su NIP.')
        _valida(not user.Uprofile.check_password(nip),
                'El NIP es incorrecto.')
        _valida(monto <= 0 or monto is None,
                'Únicamente montos positivos o válidos.')
        _valida(saldo_inicial_usuario - (monto + comision) < 0,
                'Saldo insuficiente.')
        _valida(
            not LimiteTrans(user.id).ret_efectivo_dia(float(monto)),
            'Límite transaccional superado'
        )

        clave_ordenante = ""
        clabe = UserProfile.objects.get(user=user).cuentaClabe
        for digito in clabe:
            if digito != "0":
                clave_ordenante += digito

        # hoy = datetime.now()
        # tiempo = time(15, 00, 00)
        # _valida(
        #     not (
        #         hoy.weekday() in range(
        #             0, 5) and datetime.now().time() <= tiempo),
        #     'Fuera del horario de operacion')
        # _valida(hoy.weekday() in range(5, 7), 'No se opera fines de semana')

        fecha = utc_to_local(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')
        claveR = randomString()
        status = StatusTrans.objects.get(nombre="esperando respuesta")
        tipo = TipoTransaccion.objects.get(codigo=6)
        reservado_scotia_trans = round(monto, 2)
        fecha_t = utc_to_local(timezone.now()).strftime("%Y%m%d")

        # Se crea transacción padre sólo por la comisión
        main_trans = Transaccion.objects.create(
            user=user,
            fechaValor=fecha,
            monto=float(float(monto) + comision),
            statusTrans=status,
            tipoTrans=tipo,
            concepto="Retiro Scotiabank",
            claveRastreo=claveR
        )

        # Se crea saldo reservado sólo del monto sin comisión
        scotia_retiro_reservado = SaldoReservado.objects.create(
            tipoTrans=tipo,
            status_saldo="reservado",
            saldo_reservado=reservado_scotia_trans
        )

        scotia_retiro = ScotiaRetiro.objects.create(
            ordenante=user,
            transaccion=main_trans,
            monto=Decimal(monto),
            conceptoPago="Retiro Cliente",
            ubicacion=ubicacion,
            comision=Decimal(comision),
            clave_retiro=str(clave_ordenante),
            saldoReservado=scotia_retiro_reservado,
            referenciaPago=str(fecha_t) + "{}".format(
                '{:0>8}'.format(main_trans.id))
        )

        # Quitamos el saldo que ya reservamos y el cobro de la comisión
        user.Uprofile.saldo_cuenta = round(
            float(saldo_inicial_usuario) - float(
                float(reservado_scotia_trans) + float(comision)), 2)
        user.Uprofile.save()

        return CreateRetiroScotia(
            scotia_retiro=scotia_retiro,
            user=user
        )


class CreateScotiaDeposito(graphene.Mutation):

    """
    DATA:
      mutation {
        createScotiaDeposito(
            token: {token},
            monto: 20.01,
            ubicacion: "aaaaa") {
          scotiaDeposito {
            id,
            statusTrans,
            fechaInicial,
            referenciaCobranza,
            importeDocumento,
            comision,
            fechaLimite,
            transaccion {
              id,
              monto,
              concepto,
              claveRastreo
            }
          }
        }
      }

    RESPONSE:
        {
            "data": {
                "createScotiaDeposito": {
                "scotiaDeposito": {
                    "id": "1",
                    "statusTrans": "A_0",
                    "fechaInicial": "2022-05-27",
                    "referenciaCobranza": "64618019000000007434989049",
                    "importeDocumento": 20.01,
                    "comision": 17.68,
                    "fechaLimite": "2022-05-27",
                    "transaccion": null
                }
                }
            }
        }
    """

    scotia_deposito = graphene.Field(ScotiaDepositoType)
    user = graphene.Field(UserUType)

    class Arguments:
        token = graphene.String(required=True)
        monto = graphene.Float(required=True)
        nip = graphene.String()
        ubicacion = graphene.String()

    @login_required
    def mutate(self,
               info,
               token,
               monto,
               nip,
               ubicacion=None):

        def validar(expr, msg):
            if expr:
                raise Exception(msg)

        ordenante = info.context.user

        validar(UserProfile.objects.filter(
            user=ordenante).count() == 0, 'Usuario sin perfil')
        validar(ordenante.Uprofile.password is None,
                'El usuario no ha establecido su NIP.')
        validar(not ordenante.Uprofile.check_password(nip),
                'El NIP es incorrecto.')
        validar(monto == 0 or monto is None, 'Ingrese un monto válido')
        validar(
            not LimiteTrans(ordenante.id).dep_efectivo_mes(float(monto)),
            'Límite transaccional superado'
        )
        validar(
            not LimiteTrans(ordenante.id).dep_efectivo_dia(float(monto)),
            'Límite transaccional superado'
        )

        hoy = timezone.now().date()

        num_depo = ScotiaDeposito.objects.filter(
            ordenante=ordenante,
            fecha_limite=hoy,
            importe_documento=(monto)).count()
        referencia_cobranza = genera_linea_de_captura(
            ordenante.Uprofile.cuentaClabe,
            hoy,
            float(float(monto)),
            num_depo + 1
        )
        fecha = utc_to_local(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')
        claveR = randomString()
        status = StatusTrans.objects.get(nombre="esperando respuesta")
        tipo = TipoTransaccion.objects.get(codigo=3)
        main_trans = Transaccion.objects.create(
            user=ordenante,
            fechaValor=fecha,
            monto=float(monto),
            statusTrans=status,
            tipoTrans=tipo,
            concepto="Depósito Cliente",
            claveRastreo=claveR
        )
        scotia_deposito = ScotiaDeposito.objects.create(
            ordenante=ordenante,
            importe_documento=Decimal(float(float(monto))),
            fecha_limite=hoy,
            comision=0,
            referencia_cobranza=referencia_cobranza,
            fecha_inicial=hoy,
            ubicacion=ubicacion,
            transaccion=main_trans
        )
        return CreateScotiaDeposito(
            scotia_deposito=scotia_deposito,
            user=ordenante
        )


class Mutation(graphene.ObjectType):
    create_scotia_transferencia = CreateTransferenciaScotia.Field()
    create_scotia_retiro = CreateRetiroScotia.Field()
    create_scotia_deposito = CreateScotiaDeposito.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
