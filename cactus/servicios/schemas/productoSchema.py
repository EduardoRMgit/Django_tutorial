import graphene
from graphene_django.types import DjangoObjectType
from servicios.models.productos import Productos


class TipoProductosType(DjangoObjectType):
    class Meta:
        model = Productos


class Query(object):
    """
        ``tipoProducto (Query): Query a single object from the \
        TipoTelefono Model``

        Arguments:
            - Id(int): pk from the Productos model object

    >>> Query Example:
    query{
        tipoProducto(id:30){
            id
            Servicio
            Producto
            idServicio
        }
    }

    >>> Response:
    {
        "data": {
            "tipoProducto": {
            "id": "30",
            "Servicio": "Bitdefender",
            "Producto": "Bitdefender Internet Security 1 ano",
            "idServicio": 670
            }
        }
     }


    ``allProductos (Query): Query all objects from the \
      Productos Model``

        Arguments:
            - None

        Fields to query:
            - Same from tipoProductos query

    >>> query{
        allProductos{
        id
        Servicio
        Producto
        idServicio
        idProducto
        idCattiposervicio
        TipoFront
        hasDigitToVerificator
        Precio
        ShowAyuda
        Comision
        TipoReferencia
        }
    }

    >>> Response:
    {
        "data": {
            "allProductos": [
            {
        "id": "1",
        "Servicio": "Acuario Inbursa CDMX",
        "Producto": "Acuario CDMX 1 Entrada",
        "idServicio": 899,
        "idProducto": 6443,
        "idCattiposervicio": null,
        "TipoFront": null,
        "hasDigitToVerificator": false,
        "Precio": 215,
        "ShowAyuda": true,
        "Comision": null,
        "TipoReferencia": null
      },
      {
        "id": "2",
        "Servicio": "Acuario Inbursa CDMX",
        "Producto": "Acuario CDMX 2 Entradas",
        "idServicio": 899,
        "idProducto": 6448,
        "idCattiposervicio": null,
        "TipoFront": null,
        "hasDigitToVerificator": false,
        "Precio": 430,
        "ShowAyuda": true,
        "Comision": null,
        "TipoReferencia": null
      },
      .
      .
      .

    """
    tipo_producto = graphene.Field(TipoProductosType,
                                   id=graphene.Int(),
                                   producto=graphene.String())
    all_productos = graphene.List(TipoProductosType,
                                  description="`Query all objects \
                                  from Productos Model`")

    def resolve_all_productos(self, info, **kwargs):
        return Productos.objects.all()

    def resolve_tipo_producto(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Productos.objects.get(pk=id)

        return None
