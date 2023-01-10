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
