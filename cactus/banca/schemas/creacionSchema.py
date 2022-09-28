import graphene
from graphql_jwt.decorators import login_required
from demograficos.models import Fecha
from datetime import datetime, timedelta


class HistoryType(graphene.ObjectType):
    month = graphene.String()
    year = graphene.String()


class Query(object):
    history_trans = graphene.List(HistoryType,
                                  token=graphene.String(required=True))

    '''
    Example:
    query{historyTrans(token: "")}
    Data:
    {
  "data": {
    "historyTrans": [
      {
        "month": "10",
        "year": "2021"
      },
      {
        "month": "11",
        "year": "2021"
      },
      {
        "month": "12",
        "year": "2021"
      },
      {
        "month": "01",
        "year": "2022"
      },
      {
        "month": "02",
        "year": "2022"
      },
      {
        "month": "03",
        "year": "2022"
      },
      {
        "month": "04",
        "year": "2022"
      },
      {
        "month": "05",
        "year": "2022"
      },
      {
        "month": "06",
        "year": "2022"
      },
      {
        "month": "07",
        "year": "2022"
      },
      {
        "month": "08",
        "year": "2022"
      },
      {
        "month": "09",
        "year": "2022"
      }
    ]
  }
}
    '''

    @login_required
    def resolve_history_trans(root, info, **kwargs):
        try:
            user = info.context.user
            if not user.is_anonymous:
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
                  mes = smonth - rmonth
                  if mes == 0:
                    mes = 1
                for x in range(0, mes):
                    dicc = {}
                    end = start - timedelta(days=1)
                    start = end.replace(day=1)
                    dicc['month'] = str(start.date().month).zfill(2)
                    dicc['year'] = start.date().year
                    listf.append(dicc)
                listf = reversed(listf)
                return listf
        except Exception:
            raise Exception('Bad Credentials')
