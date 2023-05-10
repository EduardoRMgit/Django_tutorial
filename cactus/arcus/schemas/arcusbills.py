import graphene
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType
from arcus.models import ServicesArcus, RecargasArcus
from demograficos.models import UserProfile
from arcus.utils.autharcus import headers_arcus
import requests
from django.conf import settings
import json


class ServicesType(DjangoObjectType):
    class Meta:
        model = ServicesArcus


class RecargasType(DjangoObjectType):
    class Meta:
        model = RecargasArcus


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
    def resolve_services_bills(root, token,
                               limit=None,
                               offset=None, tipo=None, nombre=None):
        all = ServicesArcus.objects.all()
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
    def resolve_recargas_bills(root, token,
                               limit=None, offset=None):
        all = RecargasArcus.objects.all()
        if offset:
            all = all[offset:]
        if limit:
            all = all[:limit]
        return all


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
        biller_id = graphene.String(required=True)
        account_number = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, biller_id, account_number):
        try:
            user = info.context.user
        except Exception:
            raise Exception('Usuario Inexistente')

        try:
            UserProfile.objects.filter(user=user)[0]
        except Exception:
            raise Exception('Usuario sin perfil')

        try:
            headers = headers_arcus("/bills")
            url = f"{settings.ARCUS_DOMAIN}/bills"
            data = {}
            data["biller_id"] = biller_id
            data["account_number"] = account_number
            response = requests.post(url=url, headers=headers, json=data)
        except Exception as error:
            raise Exception("Error en la peticion", error)
        response = (json.loads(response.content.decode("utf-8")))
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
