import graphene
from graphene_django.types import DjangoObjectType

from demograficos.models.documentos import (DocAdjuntoTipo,
                                            DocAdjunto,
                                            TipoComprobante)


class DocAdjuntoTipoType(DjangoObjectType):
    class Meta:
        model = DocAdjuntoTipo


class DocAdjuntoType(DjangoObjectType):
    class Meta:
        model = DocAdjunto


class TipoComprobanteType(DjangoObjectType):
    class Meta:
        model = TipoComprobante


class Query(object):
    """

    ``docAdjuntoTipo (Query): Query a single object from DocAdjuntoTipo Model``

        Arguments:
            - docAdjuntoTipoId (int): pk of the DocAdjuntoTipo Model Object
            - tipo (string): name/kind of the document

        Fields to query:
            - id
            - tipo
            - tipoDocumento

    >>> Query Example:
    query{
        docAdjuntoTipo(docAdjuntoTipoId:1) {
            id
                tipo
            tipoDocumento {
                id
            }
        }
    }


    >>> Response:
    {
        "data": {
            "docAdjuntoTipo": {
            "id": "1",
            "tipo": "INE",
            "tipoDocumento": [
                    {
                        "id": "1"
                    },
                    {
                        "id": "4"
                    }
                ]
            }
        }
    }


    ``AllDocAdjuntoTipo (Query): Query all objects from DocAdjuntoTipo Model``

        Arguments:
            - None

        Fields to query:
            - same from DocAdjuntoTipo

    >>> Query Example:
    query{
        allDocAdjuntoTipo {
            id
            tipo
        }
    }

    >>> Response:
    {
        "data": {
            "allDocAdjuntoTipo": [
                {
                    "id": "1",
                    "tipo": "INE"
                },
                {
                    "id": "2",
                    "tipo": "INE REVERSO"
                },
                {
                    "id": "3",
                    "tipo": "COMPROBANTE DE DOMICILIO"
                }
            ]
        }
    }


    ``docAdjunto (Query): Query a single object from DocAdjunto Model``

        Arguments:
            - docAdjuntoId (int): pk of the DocAdjunto Model Object

        Fields to query:
            - id
            - ruta
            - tipo
            - validado
            - user
            - orden
            - fechaCreado
            - ine
            - ineReverso
            - comprobanteDom

    >>> Query Example:
    query{
        docAdjunto (docAdjuntoId:1){
            id
            imagen
            ruta
            tipo {
                id
            }
            validado
            user {
                id
            }
            orden
            fechaCreado
            ine {
                blockedDate
                fechaNacimiento
            }
            ineReverso {
                blockedDate
                fechaNacimiento
            }
            comprobanteDom {
                blockedDate
                fechaNacimiento
            }
        }
    }

    >>> Response:
    {
        "data": {
            "docAdjunto": {
            "id": "1",
            "imagen": "",
            "ruta": "www.urldeamazonS3.com",
            "tipo": {
                "id": "1"
            },
            "validado": true,
            "user": {
                "id": "1"
            },
            "orden": true,
            "fechaCreado": "2019-08-13T19:02:23.845000+00:00",
            "ine": [
                {
                    "blockedDate": null,
                    "fechaNacimiento": "2019-08-13"
                }
            ],
            "ineReverso": [],
            "comprobanteDom": []
            }
        }
    }

    ``allDocAdjunto (Query): Query all objects from DocAdjunto Model``

        Arguments:
            - None

        Fields to query:
            - Same from docAdjunto query

    >>> Query Example:
    query{
        allDocAdjunto{
            id
            ruta
            tipo {
                tipo
            }
        }
    }


    >>> Response:
    {
        "data": {
            "allDocAdjunto": [
            {
                "id": "1",
                "ruta": "www.urldeamazonS3.com",
                "tipo": {
                "tipo": "INE"
                }
            },
            {
                "id": "2",
                "ruta": "www.rutadeinereverso.com",
                "tipo": {
                "tipo": "INE REVERSO"
                }
            },
            {
                "id": "3",
                "ruta": "www.rutadefotodecomprobantededomicilio.com",
                "tipo": {
                "tipo": "COMPROBANTE DE DOMICILIO"
                }
            },
            {
                "id": "4",
                "ruta": "WWW.OTRARUTADEINE.COM",
                "tipo": {
                "tipo": "INE"
                }
            },
            {
                "id": "5",
                "ruta": "www.rutadeinereversodos.com",
                "tipo": {
                "tipo": "INE REVERSO"
                }
            },
            {
                "id": "6",
                "ruta": "www.comprobantededom.com",
                "tipo": {
                "tipo": "COMPROBANTE DE DOMICILIO"
                }
            }
            ]
        }
    }

    """
    doc_adjunto_tipo = graphene.Field(DocAdjuntoTipoType,
                                      doc_adjunto_tipo_id=graphene.Int(),
                                      tipo=graphene.String(),
                                      description="`Query a single object from\
                                        DocAdjuntoTipo Model:` using \
                                        docAdjuntoTipoId(pk) or tipo(string)")
    all_doc_adjunto_tipo = graphene.List(DocAdjuntoTipoType,
                                         description="`Query all objects from \
                                        DocAdjuntoTipo Model`")

    doc_adjunto = graphene.Field(DocAdjuntoType,
                                 doc_adjunto_id=graphene.Int(),
                                 description="`Query a single object from \
                                 DocAdjunto Model:` using docAdjuntoId(pk)")
    all_doc_adjunto = graphene.List(DocAdjuntoType,
                                    description="`Query all objects from \
                                    DocAdjunto Model`")
    all_tipo_comprobante = graphene.List(TipoComprobanteType,
                                         description="Query all objects from \
                                         TipoComprobante Model")

    def resolve_all_doc_adjunto_tipo(self, info, **kwargs):
        return DocAdjuntoTipo.objects.all()

    def resolve_all_doc_adjunto(self, info, **kwargs):
        return DocAdjunto.objects.all()

    # Initiatig resolvers
    def resolve_doc_adjunto_tipo(self, info, **kwargs):
        id = kwargs.get('doc_adjunto_tipo_id')
        tipo = kwargs.get('tipo')

        if id is not None:
            return DocAdjuntoTipo.objects.get(pk=id)

        if tipo is not None:
            return DocAdjuntoTipo.objects.get(tipo=tipo)

        return None

    def resolve_doc_adjunto(self, info, **kwargs):
        id = kwargs.get('doc_adjunto_id')

        if id is not None:
            return DocAdjunto.objects.get(pk=id)

        return None

    def resolve_all_tipo_comprobante(self, info, **kwargs):
        return TipoComprobante.objects.all()


class CreateDocumento(graphene.Mutation):
    """
    ``CreateDocumento (Mutation): Creates an Document``

    Arguments:
        - imagen (string): path to the location of the image.
        - ruta (string): url returned by the storage service provider.
        - tipo (string): many to one to the DocAdjuntoTipo model.
        - validado (boolean): if it's been approved by the OCR system or the \
            authorities.
        - orden (boolean): 1 equals the front of the document, 0 equals the \
            reverse face of the document.
        - fechaCreado (datetime): 1 equals the front of the document, 0 \
            equals the reverse face of the document.


    >>> Mutation Example:
    mutation{
        createDocumento(tipo: 1, imagen: "demograficos/docs/'
            \'credencial-actual.jpg"){
            documento{
                    user{
                        id
                        username
                    }
                    imagen
                    tipo{
                        id
                    }
                    validado
                    orden
                    fechaCreado
                }
            }
        }

    >>> Response:
    {
        "data": {
            "createDocumento": {
                "documento": {
                    "user": {
                    "id": "1"
                        "javierpiedra"
                    }
                    "imagen": "demograficos/docs/credencial-actual.jpg"
                    "tipo": {
                        "id": "1"
                    },
                    "validado": "false"
                    "orden": "true"
                    "fechaCreado": "2019-08-20T22:42:57.325361+00:00"
                }
            }
        }
    }

    """
    documento = graphene.Field(DocAdjuntoType)

    class Arguments:
        imagen = graphene.String(required=True)
        # ruta = graphene.String()
        tipo = graphene.Int(required=True)
        validado = graphene.String()
        orden = graphene.String()
        fechaCreado = graphene.String()

    def mutate(self, info, tipo, imagen, validado=False,  # ruta=None
               orden=False, fechaCreado=None):
        documento = DocAdjunto.objects.create(imagen=imagen,
                                              # ruta=ruta,
                                              tipo=DocAdjuntoTipo.objects.get(
                                                pk=tipo),
                                              validado=validado,
                                              orden=orden,
                                              fechaCreado=fechaCreado,
                                              user=info.context.user)

        return CreateDocumento(documento=documento)


class UpdateDocumento(graphene.Mutation):
    documento = graphene.Field(DocAdjuntoType)

    class Arguments:
        imagen = graphene.String(required=True)
        # ruta = graphene.String()
        tipo = graphene.Int(required=True)
        validado = graphene.String()
        orden = graphene.String()
        fechaCreado = graphene.String()

    def mutate(self, info, tipo, imagen, validado=False,  # ruta=None
               orden=False, fechaCreado=None):
        documento = UpdateDocumento.objects.get(pk=id)
        if imagen:
            documento.imagen = imagen
        # if ruta:
        #     documento.imagen = ruta
        if tipo:
            documento.relacion = tipo
        if validado:
            documento.validado = validado
        if orden:
            documento.orden = orden
        if fechaCreado:
            documento.fechaCreado = fechaCreado

        DocAdjunto.save()

        return UpdateDocumento(documento=documento)


class Mutation(graphene.ObjectType):
    create_documento = CreateDocumento.Field()
    update_documento = UpdateDocumento.Field()
