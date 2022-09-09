import graphene
import graphql_jwt
from servicios.schemas import productoSchema, GpoTRansaccionSchema
from legal.schemas import legalSchema
from banca.schemas import transaccionSchema, inguzSchema, ScotiaSchema
from demograficos.schemas import (userProfileSchema,
                                  telefonoSchema,
                                  tarjetaSchema,
                                  institucionesSchema,
                                  documentosSchema,
                                  direccionSchema,
                                  locationSchema)
from spei.schemas import listabancosSchema
from seguros.schemas import asignar_seguro
from dde.schemas import (createddeSchema, imagenesddeSchema)
from pagos.rapydcollect import schemacollect


class Query(transaccionSchema.Query,
            productoSchema.Query,
            userProfileSchema.Query,
            telefonoSchema.Query,
            tarjetaSchema.Query,
            institucionesSchema.Query,
            direccionSchema.Query,
            documentosSchema.Query,
            legalSchema.Query,
            listabancosSchema.Query,
            locationSchema.Query,
            schemacollect.Query,
            ScotiaSchema.Query,
            graphene.ObjectType):
    pass


class Mutation(transaccionSchema.Mutation,
               userProfileSchema.Mutation,
               direccionSchema.Mutation,
               documentosSchema.Mutation,
               legalSchema.Mutation,
               telefonoSchema.Mutation,
               asignar_seguro.Mutation,
               GpoTRansaccionSchema.Mutation,
               createddeSchema.Mutation,
               imagenesddeSchema.Mutation,
               schemacollect.Mutation,
               inguzSchema.Mutation,
               ScotiaSchema.Mutation,
               graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
