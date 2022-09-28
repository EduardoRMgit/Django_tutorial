import io
import calendar
from datetime import datetime
from weasyprint import HTML

from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.files.base import ContentFile

import graphene
from graphql import GraphQLError
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from demograficos.models.userProfile import UserProfile
from legal.models.pdfLegal import PdfLegal, PdfLegalUser

from banca.views.transactionView import (build_html_cuenta,
                                         upload_s3, parse_dates_cuenta)


class PdfLegalType(DjangoObjectType):
    class Meta:
        model = PdfLegal


class UProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile


class Query(object):
    """

    ``PdfLegal (Query): Query a single object from PdfLegalType Model``

        Arguments:
            - PdfLegalId (int): pk of the PdfLegal Model Object
            - tipo (string): name/kind of the document

        Fields to query:
            - id
            - nombre

    >>> Query Example:
    query{
        pdfLegal(id:6) {
            id
            nombre
        }
    }

    >>> Response:
    {
      "data": {
        "pdfLegal": {
          "id": "6",
          "nombre": "Autorizacion zygoo"
        }
      }
    }
    """
    pdfLegal = graphene.Field(PdfLegalType,
                              id=graphene.Int(required=True),
                              description="`Query a single object from \
                                PdfLegalType Model:` using pdfLegalId(pk)")

    all_pdfLegal = graphene.List(PdfLegalType,
                                 description="`Query all objects from \
                                 pdfLegal Model`")

    def resolve_pdfLegal(self, info, **kwargs):
        return PdfLegal.objects.get(id=kwargs['id'])

    def resolve_all_pdfLegal(self, info, **kwargs):
        return PdfLegal.objects.all()


class FlagKitLegal(graphene.Mutation):
    """
    ``FlagKitLegal (Mutation): Flags UserProfile if the User agrees with legal
      kit``
    """
    profile = graphene.Field(UProfileType)

    class Arguments:
        token = graphene.String(required=True)
        nip = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, nip):
        try:
            user = info.context.user
        except Exception:
            raise Exception('Usuario Inexistente')

        try:
            profile = UserProfile.objects.filter(user=user)[0]
        except Exception:
            raise Exception('Usuario sin perfil')

        # TODO que se cheque el nip encriptado
        # if(not user.Uprofile.check_password(nip)):
        if not user.Uprofile.nip == nip:
            raise Exception('Nip esta mal')

        profile.aceptaContrato = True
        profile.save()

        return FlagKitLegal(profile=profile)


class UrlPdfLegal(graphene.Mutation):
    """
    ``UrlPdfLegal (Mutation): Gets the signed url for the legal pdf by id
      kit``
    """
    url = graphene.String()

    class Arguments:
        id = graphene.Int()
        token = graphene.String(required=True)

    @login_required
    def mutate(self, info, token, id):

        _SWITCH_IDS = {
            1: 3,
            2: 4,
            3: 2,
            4: 1
        }
        _ID = _SWITCH_IDS[id]

        file_url = ""
        user = info.context.user
        benefs = user.User_Beneficiario.all()
        nombre = PdfLegal.objects.get(id=_ID)

        now = timezone.now()

        html_string = render_to_string(f'banca/{nombre}.html',
                                       {'now': now,
                                        'benefs': benefs,
                                        'user': user})

        html = HTML(string=html_string)

        result = html.write_pdf()
        # pdf_file = io.BytesIO(result)
        pdf_file = ContentFile(result, '{user}_{now}_{nombre}.pdf')

        pdf_legal = PdfLegalUser.objects.create(user=user,
                                                nombre=nombre, Pdf=pdf_file)
        # pdf_legal.Pdf = pdf_file
        # pdf_legal.save()

        pdf_legal = PdfLegalUser.objects.last()

        file_url = pdf_legal.Pdf.url
        return UrlPdfLegal(url=file_url)


class UrlEdoCuenta(graphene.Mutation):
    """
    ``UrlEdoCuenta (Mutation): Gets the signed url for the legal pdf by
      month and date, or date_from and date_to. If only the month and year
      are given, it returns a the pdf in a special estado de cuenta format``

    Arguments:
        - nip (string, required): The nip of the authorized user
        - date_from (string): From date in format: YYYY-m-d
        - date_to (string): To date in format: YYYY-m-d
        - month (string): Number of month
        - year (string): Year number

    Fields to query:
        - url: This will be the response we can get from this '\
          'mutation. The new instance of the recently created user.

    >>> Mutation Example:
    mutation{urlEdoCuenta(
      token: ""
      month: 9, nip: "123456", year: 2019) {
      url
    }}

    {
      "data": {
        "urlEdoCuenta": {
          "url": "file.pdf"
        }
      }
    }
    """
    url = graphene.String()

    class Arguments:
        nip = graphene.String(required=True)
        token = graphene.String(required=True)
        month = graphene.Int(required=True)
        year = graphene.Int(required=True)

    @login_required
    def mutate(self, info, year, nip, token='', month=''):
        user = info.context.user
        is_cuenta = False

        # We make a dict of the dates to conform to the rest method.
        req = {}
        for variable in ['nip', 'month', 'year']:
            req[variable] = eval(variable)

        nip_string = req.get("nip", "")

        if nip_string == "":
            raise GraphQLError("Nip must be given")

        try:
            if not user.Uprofile.check_password(nip_string):
                raise GraphQLError("Incorrect NIP")
        except TypeError:
            raise GraphQLError("User has no NIP")

        parser = parse_dates_cuenta(req)

        if parser[0] is None:
            date_format_error = "Either 'month' and 'year or " + \
                        "'date_from' and 'date_to'" + \
                        " must be given"
            raise GraphQLError(date_format_error)
        else:
            date_from, date_to, is_cuenta = parser

        if (date_to.month > timezone.now().month and
                date_to.year > timezone.now().year):
            raise GraphQLError("End date cannot be more than " +
                               "present month")

        last_day_of_month = calendar.monthrange(date_to.year, date_to.month)[1]
        fecha_dt = (
            str(last_day_of_month) + '/' + str(date_to.month) + '/' + str(date_to.year))  # noqa
        cut_off_date = datetime.strptime(fecha_dt, '%d/%m/%Y')

        month_period = date_from.month
        months = ['Enero', 'Febrero',
                  'Marzo', 'Abril',
                  'Mayo', 'Junio',
                  'Julio', 'Agosto', 'Septiembre',
                  'Octubre', 'Noviembre', 'Diciembre']
        month = months[month_period - 1] + ' ' + str(date_from.year)
        # Model data
        html = build_html_cuenta(user, date_from, date_to,
                                 is_cuenta, cut_off_date, month)

        result = html.write_pdf()
        file = io.BytesIO(result)

        if settings.USE_S3:
            file_url = upload_s3(file, user)
            return UrlEdoCuenta(url=file_url)
        else:
            raise GraphQLError("Debug estado cuenta" +
                               " not implented yet, set USE_S3 in .env to 1")


class Mutation(graphene.ObjectType):
    url_pdf_legal = UrlPdfLegal.Field()
    url_edo_cuenta = UrlEdoCuenta.Field()
