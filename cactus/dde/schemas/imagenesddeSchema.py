import requests
from base64 import b64encode

import graphene
from graphene_django.types import DjangoObjectType

from demograficos.models.documentos import DocAdjuntoTipo, DocAdjunto
from demograficos.models import Telefono


class Doc_AdjuntoTipoType(DjangoObjectType):
    class Meta:
        model = DocAdjuntoTipo


class Doc_AdjuntoType(DjangoObjectType):
    class Meta:
        model = DocAdjunto


class Tele_fonoType(DjangoObjectType):
    class Meta:
        model = Telefono


class uploadDocs(graphene.Mutation):
    valido = graphene.String()

    class Arguments:
        token = graphene.String(required=True)
        local = graphene.Boolean()

    def mutate(self, info, token, local=False):

        user = info.context.user
        up = user.Uprofile
        if not up.id_dde:
            raise Exception('user does not have dde_id')
        try:
            tel = Telefono.objects.get(user=user, activo=True)
        except Telefono.DoesNotExist:
            raise Exception("User must have telefono")

        url = 'https://dde.inguz.site/dde/imagetest/' if not local else  \
              'http://127.0.0.1:8001/dde/imagetest/'
        userAndPass = b64encode(b"test:t35t3r").decode("ascii")
        headers = {'Authorization': 'Basic %s' % userAndPass}
        types = ["INE", "INE REVERSO", "COMPROBANTE DE DOMICILIO"]
        file_list = []
        image_urls = []
        for type in types:
            image_url = ""
            try:
                doc_type = DocAdjuntoTipo.objects.get(tipo=type)
                doc = DocAdjunto.objects.filter(user=user, tipo=doc_type)[0]
                image_url = doc.imagen.url
                image_url = image_url[1:]
                image_urls.append(image_url)
            except Exception:
                raise Exception("No uploaded INE")
            if not local:
                response = requests.get(image_url)
                file_list.append(response.content)
            else:
                f = open(image_url, 'rb')
                file_list.append(f)

        data = {'id': up.id_dde, 'telefono': tel}
        files = {'ine': file_list[0], 'inereverso': file_list[1],
                 'compdomicilio': file_list[2]}
        try:
            r = requests.post(url, files=files, data=data, headers=headers)
            if r.status_code != 200:
                raise Exception(r._content)
            print(r.__dict__)
            res = "Se añadieron las imagenes"
        except Exception as e:
            raise Exception('post sin exito: ', e)
        return uploadDocs(valido=res)


class Mutation(graphene.ObjectType):
    upload_Docs = uploadDocs.Field()
