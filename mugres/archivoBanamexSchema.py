import graphene
from graphene_django.types import DjangoObjectType

from banca.models.archivoBanamex import (TransPago_AuthHead,
                                         TransPago_AuthDet,
                                         UploadBNXOutSetSVA,
                                         UploadTefOut)


class TransPago_AuthHeadType(DjangoObjectType):
    class Meta:
        model = TransPago_AuthHead


class TransPago_AuthDetType(DjangoObjectType):
    class Meta:
        model = TransPago_AuthDet


class UploadBNXOutSetSVAType(DjangoObjectType):
    class Meta:
        model = UploadBNXOutSetSVA


class UploadTefOutType(DjangoObjectType):
    class Meta:
        model = UploadTefOut


class Query(object):
    """
    ``transpago_authhead (Query):
    Query a single object from transpago_authhead Model``

    ``transpago_authdet (Query):
    Query a single object from transpago_authdet Model``

    ``uploadBNXOutSetSVA (Query):
    Query a single object from uploadBNXOutSetSVA Model``

    ``uploadTefOut (Query): Query a single object from uploadTefOut Model``

    Arguments:
        -

    Fields to query:
        - id
        - nombreArchivo
        - depositoRef
        - fechaArchivo
        - fechaOperacion
        - fechaAutorizado
        - montoTotalPagos
        - numRegistros
        - institucion
        - user
        - transpagoAuthdetSet

    >>> Query Example:
    query{
        transpago_Authhead(id: "1") {
            id
            nombreArchivo
            depositoRef
            fechaArchivo
            fechaOperacion
            fechaAutorizado
            montoTotalPagos
            numRegistros
            institucion
            user {}
            transpagoAuthdetSet
            }
    >>> Response:

    """

    transpago_authhead = graphene.Field(TransPago_AuthHeadType,
                                        id=graphene.Int(),
                                        nombreArchivo=graphene.String())
    all_transpago_authhead = graphene.List(TransPago_AuthHeadType)

    transpago_authdet = graphene.Field(TransPago_AuthDetType,
                                       id=graphene.Int(),
                                       noAuth=graphene.String())
    all_transpago_authdet = graphene.List(TransPago_AuthDetType)

    uploadBNXOutSetSVA = graphene.Field(UploadBNXOutSetSVAType,
                                        id=graphene.Int())
    all_uploadBNXOutSVA = graphene.List(UploadBNXOutSetSVAType)

    uploadTefOut = graphene.Field(UploadTefOutType,
                                  id=graphene.Int())
    all_uploadTefOut = graphene.List(UploadTefOutType)

    def resolve_all_transpago_authhead(self, info, **kwargs):
        return TransPago_AuthHead.objects.all()

    def resolve_all_transpago_authdet(self, info, **kwargs):
        return TransPago_AuthDet.objects.all()

    def resolve_all_uploadBNXOutSVA(self, info, **kwargs):
        return UploadBNXOutSetSVA.objects.all()

    def resolve_all_uploadTefOut(self, info, **kwargs):
        return UploadTefOut.objects.all()

    def resolve_transpago_authhead(self, info, **kwargs):
        id = kwargs.get('id')
        nombreArchivo = kwargs.get('nombreArchivo')

        if id is not None:
            return TransPago_AuthHead.objects.get(pk=id)

        if nombreArchivo is not None:
            return TransPago_AuthHead.objects.get(nombreArchivo=nombreArchivo)

        return None

    def resolve_transpago_authdet(self, info, **kwargs):
        id = kwargs.get('id')
        noAuth = kwargs.get('noAuth')

        if id is not None:
            return TransPago_AuthDet.objects.get(pk=id)

        if noAuth is not None:
            return TransPago_AuthDet.objects.get(noAuth=noAuth)

        return None

    def resolve_uploadBNXOutSetSVA(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return UploadBNXOutSetSVA.objects.get(pk=id)

        return None

    def resolve_uploadTefOut(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return UploadBNXOutSetSVA.objects.get(pk=id)

        return None


# class CreateTransPago_AuthHead(graphene.Mutation):
#     transpago_authhead = graphene.Field(TransPago_AuthHeadType)

#     class Arguments:
#         id = graphene.Int()
#         nombreArchivo = graphene.String()
#         depositoRef = graphene.String()
#         fechaArchivo = graphene.DateTime()
#         fechaOperacion = graphene.DateTime()
#         fechaAutorizado = graphene.DateTime()
#         montoTotalPagos= graphene.Decimal()
#         numRegistros = graphene.Decimal()
#         institucion_id = Field(InstitucionType)
#         user = graphene.Field(UserProfileType)

#     #3
#     def mutate(self, info, nombreArchivo, depositoRef, fechaArchivo,
#             fechaOperacion, fechaAutorizado, montoTotalPagos, numRegistros,
#             institucion, user):

#         user = info.context.user or None
#         institucion = Institucion.objects.filter(id=institucion_id).first()

#         if not institucion:
#             raise Exception('Invalid Institucion!')

#         transpago_authhead = TransPago_AuthHead(
#             nombreArchivo=nombreArchivo,
#             depositoRef=depositoRef,
#             fechaArchivo=fechaArchivo,
#             fechaOperacion=fechaOperacion,
#             fechaAutorizado=fechaAutorizado,
#             montoTotalPagos=montoTotalPagos,
#             numRegistros=numRegistros,
#             institucion=institucion,
#             )

#         transpago_authhead.save()

#         return CreateTransPago_AuthHead(
#             id= experience.id,
#             title = experience.title,
#             owner= experience.owner,
#             category = experience.category,
#             subcategory = experience.subcategory,
#             modality = experience.modality,
#             locationRange = experience.locationRange,
#             groupSize = experience.groupSize,
#             level = experience.level,
#             minAge = experience.minAge,
#             maxAge = experience.maxAge,
#             image = experience.image,
#             description = experience.description,
#             price = experience.price,
#             currency = experience.currency,
#             )


# #4
# class Mutation(graphene.ObjectType):
#     create_experience = CreateExperience.Field()
