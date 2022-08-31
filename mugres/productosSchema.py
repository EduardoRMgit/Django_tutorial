# import graphene
# from graphene_django.types import DjangoObjectType

# from banca.models.productos import Productos
# from banca.models.archivoBanamex import TransPago_AuthHead


# class ProductosType(DjangoObjectType):
#     class Meta:
#         model = Productos


# class Query(object):
#     producto = graphene.Field(ProductosType,
#                               id=graphene.Int(),
#                               producto=graphene.String())
#     all_productos = graphene.List(ProductosType)

#     def resolve_all_produtos(self, info, **kwargs):
#         return Productos.objects.all()

#     def resolve_producto(self, info, **kwargs):
#         id = kwargs.get('id')
#         producto = kwargs.get('producto')

#         if id is not None:
#             return TransPago_AuthHead.objects.get(pk=id)

#         if producto is not None:
#             return TransPago_AuthHead.objects.get(producto=producto)

#         return None
