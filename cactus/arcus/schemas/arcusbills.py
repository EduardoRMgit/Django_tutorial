import graphene
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType
from arcus.models import ServicesArcus, RecargasArcus, PagosArcus
from banca.models import Transaccion, StatusTrans, TipoTransaccion
from arcus.utils.autharcus import headers_arcus
from spei.stpTools import randomString
from arcus.utils.erroresArcus import mensajes_error
import requests
from django.conf import settings
import json
import uuid
from django.db.models import Q
from collections import Counter
from datetime import datetime, timedelta
import logging


db_logger = logging.getLogger('db')


class ServicesType(DjangoObjectType):
    class Meta:
        model = ServicesArcus


class TopupsType(graphene.ObjectType):
    amount = graphene.Float()
    description = graphene.String()
    details = graphene.String()


class RecargasType(DjangoObjectType):
    class Meta:
        model = RecargasArcus
    topups_amounts = graphene.List(TopupsType)

    def resolve_topups_amounts(self, info):
        lista = [self.topup_amounts[0],
                 self.topup_amounts[1],
                 self.topup_amounts[2]]
        return list(lista)


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
            try:
                response = requests.post(
                    url=url, headers=headers, json=data, timeout=5)
            except Exception as t:
                msg_arcus = f"[TimeOut Arcus] Tiempo de respuesta excedido:" \
                            f" {t}"
                db_logger.error(msg_arcus)
        except Exception as error:
            raise Exception("Error en la peticion", error)
        if response.status_code != 200:
            response_error = (json.loads(response.content.decode("utf-8")))
            msg_arcus = f"[Error Arcus Consulta Bill] Respuesta " \
                        f"Arcus: {response_error}"
            db_logger.error(msg_arcus)
            mensaje = mensajes_error(response_error)
            raise Exception(mensaje)
        elif response.status_code == 200:
            response = (json.loads(response.content.decode("utf-8")))
            msg_arcus = f"[Consulta Balance Exitosa] Respuesta Arcus: " \
                        f"{response}"
            db_logger.info(msg_arcus)
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
            _s.append(pago.empresa_servicio.sku_id)
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
        now = datetime.now()
        yesterday = now - timedelta(hours=24)
        try:
            if tipo == "S":
                q = PagosArcus.objects.filter(
                        Q(fecha_creacion__gte=yesterday) & Q(
                            fecha_creacion__lte=now) & Q(
                                empresa_servicio__sku_id=company_sku) & Q(
                                    numero_cuenta=account_number) & Q(
                                            monto=monto))
            elif tipo == "R":
                q = PagosArcus.objects.filter(
                        Q(fecha_creacion__gte=yesterday) & Q(
                            fecha_creacion__lte=now) & Q(
                                empresa_recargas__sku_id=company_sku) & Q(
                                    numero_cuenta=account_number) & Q(
                                            monto=monto))
            if q is not None:
                try:
                    uid = q.last().id_externo
                    headers = headers_arcus(uid)
                except Exception:
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
            try:
                response = requests.post(
                    url=url,
                    headers=headers,
                    json=data,
                    timeout=5)
            except Exception as t:
                msg_arcus = f"[TimeOut Arcus] Tiempo de respuesta excedido:" \
                            f" {t}"
                db_logger.error(msg_arcus)

        except Exception as error:
            raise Exception("Error en la peticion", error)
        if response.status_code != 201:
            response_error = (json.loads(response.content.decode("utf-8")))
            msg_arcus = f"[Error Arcus] Respuesta arcus: {response_error} " \
                        f"peticion: {data} del usuario: {user}"
            db_logger.error(msg_arcus)
            mensaje = mensajes_error(response_error)
            raise Exception(mensaje)
        response = (json.loads(response.content.decode("utf-8")))
        fecha = datetime.strptime(response["processed_at"], '%Y-%m-%d').date()
        hora = datetime.strptime(response["process_at_time"], '%H:%M').time()
        rastreo = randomString()
        fecha = datetime.combine(fecha, hora)
        if "Pago realizado exitosamente" in response["ticket_text"]:
            status = StatusTrans.objects.get(nombre="exito")
        else:
            status = StatusTrans.objects.get(nombre="rechazada")
        try:
            if tipo == "R":
                _tipo = TipoTransaccion.objects.get(codigo=101)
                empresa = RecargasArcus.objects.get(sku_id=company_sku)
            elif tipo == "S":
                _tipo = TipoTransaccion.objects.get(codigo=100)
                empresa = ServicesArcus.objects.get(sku_id=company_sku)
        except Exception:
            raise Exception("Empresa no existe")
        concepto = response["ticket_text"]
        if len(q) == 0:
            main_trans = Transaccion.objects.create(
                user=user,
                fechaValor=fecha,
                monto=monto,
                statusTrans=status,
                tipoTrans=_tipo,
                concepto=concepto,
                claveRastreo=rastreo
            )
        if tipo == "R" and len(q) == 0:
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
                empresa_recargas=empresa
            )
        if tipo == "S" and len(q) == 0:
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
                empresa_servicio=empresa
            )
        else:
            pay = q.last()
        if status.nombre == "exito" and saldo and len(q) == 0:
            user.Uprofile.saldo_cuenta -= round(float(monto), 2)
            user.Uprofile.save()
        msg_arcus = f"[Pago Exitoso Arcus] Pago realizado exitosamente " \
                    f"transaccion: {response}"
        db_logger.info(msg_arcus)
        return ArcusPay(pay=pay)


class Mutation(graphene.ObjectType):
    arcus_pay = ArcusPay.Field()
