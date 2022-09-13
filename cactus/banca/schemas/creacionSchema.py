import graphene
from graphene_django.types import DjangoObjectType
from banca.models import Transaccion
from graphql_jwt.decorators import login_required
from demograficos.models import Fecha
from datetime import datetime, timedelta


class FechaCType(DjangoObjectType):
    class Meta:
        model = Transaccion
        fields = ('fechaValor', )


class Query(object):
    history_trans = graphene.List(graphene.String,
                                  token=graphene.String(required=True))

    '''
    Example:
    query{historyTrans(token: "")}
    Data:
    {
      "data": {
        "historyTrans": [
          "(8, 2022)",
          "(7, 2022)",
          "(6, 2022)",
          "(5, 2022)",
          "(4, 2022)",
          "(3, 2022)",
          "(2, 2022)",
          "(1, 2022)",
          "(12, 2021)",
          "(11, 2021)",
          "(10, 2021)",
          "(9, 2021)"
        ]
      }
    }
    '''

    @login_required
    def resolve_history_trans(self, info, **kwargs):
        try:
            user = info.context.user
        except Exception:
            raise Exception('Usuario Inexistente')
        listf = []
        registro = Fecha.objects.get(user=user)
        registro = registro.creacion
        start = datetime.now()
        rmonth = registro.month
        smonth = start.month
        if start.year != registro.year:
            aniosdiff = start.year - registro.year
            if aniosdiff > 1:
                mes = 12
            else:
                b = rmonth + 12
                mes = b - smonth

        else:
            mes = rmonth - smonth
        for x in range(0, mes):
            end = start - timedelta(days=1)
            start = end.replace(day=1)
            fecha = str(start.date().month).zfill(2), start.date().year
            listf.append(fecha)

        listf = reversed(listf)
        return listf
