import graphene
from graphql_jwt.decorators import login_required
from datetime import datetime


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

        user = info.context.user
        if user.is_anonymous:
            raise Exception('Usuario no válido')

        now = datetime.now()
        creation_date = user.Ufecha.creacion
        tmp_month = creation_date.month

        months = []
        for year in range(creation_date.year, now.year+1):
            while ((year < now.year and tmp_month <= 12) or
                   tmp_month < now.month):
                months.append({'month': tmp_month, 'year': year})
                tmp_month += 1
            tmp_month = 1

        if creation_date.day >= now.day:
            return months[-7:-1]

        return months[-6:]
