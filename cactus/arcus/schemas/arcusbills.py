import graphene
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType
from arcus.models import ServicesArcus, RecargasArcus, PagosArcus
from banca.models import Transaccion, StatusTrans, TipoTransaccion
from demograficos.models import UserProfile
from arcus.utils.autharcus import headers_arcus
from spei.stpTools import randomString
import requests
from django.conf import settings
import json
import uuid


class ServicesType(DjangoObjectType):
    class Meta:
        model = ServicesArcus


class RecargasType(DjangoObjectType):
    class Meta:
        model = RecargasArcus


class PagosArcusType(DjangoObjectType):
    class Meta:
        model = PagosArcus


class ConsultaBillType(graphene.ObjectType):
    balance = graphene.Float()
    company_sku = graphene.String()
    service_number = graphene.String()
    due_date = graphene.String()
    currency = graphene.String()
    periodicity = graphene.String()
    max_payment_amount = graphene.Float()
    next_payment_date = graphene.String()
    customer_fee = graphene.Float()
    customer_fee_type = graphene.String()
    bill_total = graphene.Float()


class Query(object):
    services_bills = graphene.List(ServicesType,
                                   token=graphene.String(required=True),
                                   limit=graphene.Int(),
                                   offset=graphene.Int(),
                                   tipo=graphene.String(),
                                   nombre=graphene.String(),
                                   )
    recargas_bills = graphene.List(RecargasType,
                                   token=graphene.String(required=True),
                                   limit=graphene.Int(),
                                   offset=graphene.Int())
    consult_bill = graphene.Field(ConsultaBillType,
                                  token=graphene.String(required=True),
                                  empresa=graphene.String(required=True),
                                  referencia=graphene.String(required=True))

    @login_required
    def resolve_services_bills(self, info,
                               limit=None,
                               offset=None, tipo=None, nombre=None, **kwargs):
        all = ServicesArcus.objects.all().exclude(biller_type="NO MOSTRAR")
        if nombre:
            try:
                return all.filter(name=nombre)
            except Exception:
                raise Exception("Compañia no existe.")
        if tipo:
            return all.filter(biller_type=tipo)
        if offset:
            all = all[offset:]
        if limit:
            all = all[:limit]
        return all

    @login_required
    def resolve_recargas_bills(self, info, id=None,
                               limit=None, offset=None, **kwargs):
        all = RecargasArcus.objects.all().exclude(biller_type="NO MOSTRAR")
        if id:
            all = all.filter(id_recarga=id)
        if offset:
            all = all[offset:]
        if limit:
            all = all[:limit]
        return all

    @login_required
    def resolve_consult_bill(self, info, empresa, referencia, **kwargs):
        uid = str(uuid.uuid4())
        try:
            headers = headers_arcus(uid)
            url = f"{settings.ARCUS_DOMAIN}/consult"
            data = {}
            data["company_sku"] = empresa
            data["service_number"] = referencia
            response = requests.post(url=url, headers=headers, json=data)
        except Exception as error:
            raise Exception("Error en la peticion", error)
        response = (json.loads(response.content.decode("utf-8")))
        return response


class ArcusPay(graphene.Mutation):
    pay = graphene.Field(PagosArcusType)

    class Arguments:
        token = graphene.String(required=True)
        company_sku = graphene.String(required=True)
        account_number = graphene.String(required=True)
        monto = graphene.Float(required=True)
        tipo = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, monto, company_sku, account_number):
        try:
            user = info.context.user
        except Exception:
            raise Exception('Usuario Inexistente')
        if float(monto) <= user.Uprofile.saldo_cuenta:
            saldo = True
        else:
            raise Exception("Saldo insuficiente")
        try:
            uid = str(uuid.uuid4())
            headers = headers_arcus(uid)
            url = f"{settings.ARCUS_DOMAIN}/pay"
            data = {}
            data["company_sku"] = company_sku
            data["service_number"] = account_number
            data["amount"] = monto
            data["currency"] = "MXN"
            data["external_id"] = "ec2a0bb7-deac-4c21-9ed1-042e3fe58475"
            data["payment_method"] = "DC"
            response = requests.post(url=url, headers=headers, json=data)

        except Exception as error:
            raise Exception("Error en la peticion", error)
        response = (json.loads(response.content.decode("utf-8")))
        fecha = response["processed_at"]
        hora = response["process_at_time"]
        rastreo = randomString()
        fecha = f"{fecha}T{hora}Z"
        if "Pago realizado exitosamente" in response["ticket_text"]:
            status = StatusTrans.objects.get(nombre="exito")
        else:
            status = StatusTrans.objects.get(nombre="rechazada")
        tipo = TipoTransaccion.objects.get(codigo=101)
        concepto = response["ticket_text"]
        main_trans = Transaccion.objects.create(
            user=user,
            fechaValor=fecha,
            monto=monto,
            statusTrans=status,
            tipoTrans=tipo,
            concepto=concepto,
            claveRastreo=rastreo
        )
        pay = PagosArcus.objects.create(
            tipo=tipo,
            transaccion=main_trans,
            id_transaccion=response["uid"],
            identificador=response["identifier"],
            monto=monto,
            moneda="MXN",
            comision=response["customer_fee"],
            fecha_creacion=fecha,
            estatus=response["status"],
            id_externo=response["external_id"],
            descripcion=response["ticket_text"],
            numero_telefono=response["service_number"]
        )
        if status.nombre == "exito" and saldo:
            user.Uprofile.saldo_cuenta -= round(float(monto), 2)
            user.Uprofile.save()
        return ArcusPay(pay=pay)


class Mutation(graphene.ObjectType):
    recarga_pay = PagosArcus.Field()
