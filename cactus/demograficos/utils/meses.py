def meses(mes):

    meses = (
        ("ene", "01"),
        ("feb", "02"),
        ("mar", "03"),
        ("abr", "04"),
        ("may", "05"),
        ("jun", "06"),
        ("jul", "07"),
        ("ago", "08"),
        ("sep", "09"),
        ("oct", "10"),
        ("nov", "11"),
        ("dic", "12"),
    )
    for a, b in meses:
        mes = mes.replace(a, b).replace(a, b)
    return mes


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
