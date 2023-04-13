from demograficos.utils.meses import meses


def normalizeDates(dates):

    fechas = []
    for i in dates:
        a = i.replace(dates[2], "-")
        b = a.split("-")
        b[1] = b[1][:3]
        b = "-".join(b)
        b = b.lower()
        j = meses(b)
        fechas.append(j)
    return fechas
