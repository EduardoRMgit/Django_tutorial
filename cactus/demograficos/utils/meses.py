def meses(mes):

    print('--------------------------')
    print(mes)
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
        ("ENE", "01"),
        ("FEB", "02"),
        ("MAR", "03"),
        ("ABR", "04"),
        ("MAY", "05"),
        ("JUN", "06"),
        ("JUL", "07"),
        ("AGO", "08"),
        ("SEP", "09"),
        ("OCT", "10"),
        ("NOV", "11"),
        ("DIV", "12"),
        ("Ene", "01"),
        ("Feb", "02"),
        ("Mar", "03"),
        ("Abr", "04"),
        ("May", "05"),
        ("Jun", "06"),
        ("Jul", "07"),
        ("Ago", "08"),
        ("Sep", "09"),
        ("Oct", "10"),
        ("Nov", "11"),
        ("Dic", "12")
    )
    for a, b in meses:
        print(mes)
        mes = mes.replace(a, b).replace(a, b)
    return mes
