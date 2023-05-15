import graphene
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType
from arcus.models import ServicesArcus, RecargasArcus, TiempoAire
from banca.models import Transaccion, StatusTrans, TipoTransaccion
from demograficos.models import UserProfile
from arcus.utils.autharcus import headers_arcus
import requests
from django.conf import settings
from spei.stpTools import randomString
import json
import uuid


class ServicesType(DjangoObjectType):
    class Meta:
        model = ServicesArcus


class RecargasType(DjangoObjectType):
    class Meta:
        model = RecargasArcus


class TiempoAireType(DjangoObjectType):
    class Meta:
        model = TiempoAire


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


class RecargaPay(graphene.Mutation):
    recarga = graphene.Field(TiempoAireType)

    class Arguments:
        token = graphene.String(required=True)
        biller_id = graphene.String(required=True)
        account_number = graphene.String(required=True)
        monto = graphene.Int(required=True)

    @login_required
    def mutate(self, info, token, monto, biller_id, account_number):
        try:
            user = info.context.user
        except Exception:
            raise Exception('Usuario Inexistente')
        try:
            headers = headers_arcus("/single/pay")
            url = f"{settings.ARCUS_DOMAIN}/single/pay"
            data = {}
            data["biller_id"] = biller_id
            data["account_number"] = account_number
            data["amount"] = monto
            data["currency"] = "MXN"
            data["external_id"] = randomString()
            data["pos_number"] = ""
            response = requests.post(url=url, headers=headers, json=data)

        except Exception as error:
            raise Exception("Error en la peticion", error)
        response = (json.loads(response.content.decode("utf-8")))
        fecha = response["created_at"]
        if "Pago realizado exitosamente" in response["ticket_text"]:
            status = StatusTrans.objects.get(nombre="exito")
        else:
            status = StatusTrans.objects.get(nombre="rechazada")
        tipo = TipoTransaccion.objects.get(codigo=101)
        if float(monto) <= user.Uprofile.saldo_cuenta and \
                status.nombre == "exito":
            user.Uprofile.saldo_cuenta -= round(float(monto), 2)
            user.Uprofile.save()
        else:
            raise Exception("Saldo insuficiente")
        concepto = response["ticket_text"]
        main_trans = Transaccion.objects.create(
            user=user,
            fechaValor=fecha,
            monto=monto,
            statusTrans=status,
            tipoTrans=tipo,
            concepto=concepto
        )
        recarga = TiempoAire.objects.create(
            transaccion=main_trans,
            id_transaccion=response["id"],
            monto=monto,
            moneda="MXN",
            monto_usd=response["amount_usd"],
            comision=response["transaction_fee"],
            total_usd=response["total_usd"],
            fecha_creacion=fecha,
            estatus=response["status"],
            id_externo=response["external_id"],
            descripcion=response["ticket_text"],
            numero_telefono=response["account_number"]
        )
        return RecargaPay(recarga=recarga)


class CreateBill(graphene.Mutation):

    type = graphene.String()
    id = graphene.String()
    biller_id = graphene.Int()
    account_number = graphene.String()
    name_on_account = graphene.String()
    due_date = graphene.String()
    balance = graphene.Float()
    balance_currency = graphene.String()
    balance_updated_at = graphene.String()
    error_code = graphene.String()
    error_message = graphene.String()
    status = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        company_sku = graphene.String(required=True)
        account_number = graphene.String()
        mount = graphene.Float()

    @login_required
    def mutate(self, info, token, company_sku, account_number):
        try:
            user = info.context.user
        except Exception:
            raise Exception('Usuario Inexistente')

        try:
            UserProfile.objects.filter(user=user)[0]
        except Exception:
            raise Exception('Usuario sin perfil')

        try:
            headers = headers_arcus()
            url = f"{settings.ARCUS_DOMAIN}/consult"
            print(url)
            print(headers)
            data = {}
            data["company_sku"] = company_sku
            data["service_number"] = account_number
            data["client_id"] = "3"
            # data["amount"] = amount
            # data["currency"] = "MXN"
            # data["external_id"] = str(uuid.uuid4())
            # data["payment_method"] = "DC"
            response = requests.post(url=url, headers=headers, json=data)
        except Exception as error:
            raise Exception("Error en la peticion", error)
        print(response)
        response = (json.loads(response.content.decode("utf-8")))
        print(response)
        return CreateBill(type=response["type"],
                          id=response["id"],
                          biller_id=response["biller_id"],
                          account_number=response["account_number"],
                          name_on_account=response["name_on_account"],
                          due_date=response["due_date"],
                          balance=response["balance"],
                          balance_currency=response["balance_currency"],
                          balance_updated_at=response["balance_updated_at"],
                          error_code=response["error_code"],
                          error_message=response["error_message"],
                          status=response["status"])


class Mutation(graphene.ObjectType):
    create_bill = CreateBill.Field()
    recarga_pay = RecargaPay.Field()
