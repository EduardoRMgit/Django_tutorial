import graphene
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType
from arcus.models import ServicesArcus, RecargasArcus, PagosArcus
from banca.models import Transaccion, StatusTrans, TipoTransaccion
from arcus.utils.autharcus import headers_arcus
from spei.stpTools import randomString
import requests
from django.conf import settings
import json
import uuid
from django.db.models import Q
from collections import Counter
from datetime import datetime, time


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
                                   offset=graphene.Int(),
                                   tipo=graphene.String(),
                                   nombre=graphene.String())
    consult_bill = graphene.Field(ConsultaBillType,
                                  token=graphene.String(required=True),
                                  empresa=graphene.String(required=True),
                                  referencia=graphene.String(required=True))
    pagos_recurrentes = graphene.List(ServicesType,
                                      token=graphene.String(required=True))

    @login_required
    def resolve_services_bills(self, info,
                               limit=None,
                               offset=None, tipo=None, nombre=None, **kwargs):
        qs = ServicesArcus.objects.all().exclude(biller_type="NO MOSTRAR")

        if nombre:
            filter = (
                Q(name__icontains=nombre)
            )
            qs = qs.filter(filter)
        if tipo:
            filter = (
                Q(biller_type__icontains=tipo)
            )
            qs = qs.filter(filter)
        if offset:
            qs = qs[offset:]
        if limit:
            qs = qs[:limit]
        return qs

    @login_required
    def resolve_recargas_bills(self, info, id=None, nombre=None, tipo=None,
                               limit=None, offset=None, **kwargs):
        qs = RecargasArcus.objects.all().exclude(biller_type="NO MOSTRAR")
        if nombre:
            filter = (
                Q(name__icontains=nombre)
            )
            qs = qs.filter(filter)
        if tipo:
            filter = (
                Q(biller_type__icontains=tipo)
            )
            qs = qs.filter(filter)
        if id:
            filter = (
                Q(id_recarga__exact=id)
            )
        if offset:
            qs = qs[offset:]
        if limit:
            qs = qs[:limit]
        return qs

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

    @login_required
    def resolve_pagos_recurrentes(self, info, token, **kwargs):
        try:
            user = info.context.user
        except Exception:
            raise Exception('Usuario Inexistente')
        tipo = "S"
        status = "successful"
        _s = []
        recurrente_ = []
        pagos = PagosArcus.objects.filter(
            usuario=user, tipo=tipo, estatus=status)
        for pago in pagos:
            _s.append(pago.empresa.sku_id)
        recurrentes = list(Counter(_s))[:5]
        for recurrente in recurrentes:
            recurrente_.append(ServicesArcus.objects.get(sku_id=recurrente))
        return recurrente_


class ArcusPay(graphene.Mutation):
    pay = graphene.Field(PagosArcusType)

    class Arguments:
        token = graphene.String(required=True)
        company_sku = graphene.String(required=True)
        account_number = graphene.String(required=True)
        monto = graphene.Float(required=True)
        tipo = graphene.String(required=True)
        nip = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, monto,
               company_sku, account_number, tipo, nip):
        try:
            user = info.context.user
        except Exception:
            raise Exception('Usuario Inexistente')
        if not user.Uprofile.password:
            raise Exception("Usuario no ha establecido nip")
        if not user.Uprofile.check_password(nip):
            raise Exception('Nip incorrecto')
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
            data["external_id"] = uid
            data["payment_method"] = "DC"
            response = requests.post(url=url, headers=headers, json=data)

        except Exception as error:
            raise Exception("Error en la peticion", error)
        response = (json.loads(response.content.decode("utf-8")))
        print(response)
        fecha = datetime.strptime(response["processed_at"], '%Y-%m-%d').date()
        hora = datetime.strptime(response["process_at_time"], '%H:%M').time()
        rastreo = randomString()
        fecha = datetime.combine(fecha, hora)
        if "Pago realizado exitosamente" in response["ticket_text"]:
            status = StatusTrans.objects.get(nombre="exito")
        else:
            status = StatusTrans.objects.get(nombre="rechazada")
        if tipo == "R":
            _tipo = TipoTransaccion.objects.get(codigo=101)
        elif tipo == "S":
            _tipo = TipoTransaccion.objects.get(codigo=100)
        try:
            empresa = ServicesArcus.objects.get(sku_id=company_sku)
        except Exception:
            raise Exception("Empresa no existe")
        concepto = response["ticket_text"]
        main_trans = Transaccion.objects.create(
            user=user,
            fechaValor=fecha,
            monto=monto,
            statusTrans=status,
            tipoTrans=_tipo,
            concepto=concepto,
            claveRastreo=rastreo
        )
        pay = PagosArcus.objects.create(
            tipo=tipo,
            usuario=user,
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
            numero_cuenta=response["service_number"],
            empresa=empresa
        )
        if status.nombre == "exito" and saldo:
            user.Uprofile.saldo_cuenta -= round(float(monto), 2)
            user.Uprofile.save()
        return ArcusPay(pay=pay)


class Mutation(graphene.ObjectType):
    arcus_pay = ArcusPay.Field()
