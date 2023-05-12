

def categorias(categoria, name):
    if categoria == "Cable" or \
            categoria == "PostPaidCell" and \
            name != "Juego total":
        categoria = "INTERNET/TV"
    elif categoria == "Electricity" and name == "CFE":
        categoria = "LUZ"
    elif categoria == "Gas":
        categoria = "GAS"
    elif categoria == "Government" or \
            categoria == "Insurance" or  \
            categoria == "Media Subscription" or \
            categoria == "Mortgage":
        categoria = "OTROS"
    elif categoria == "Toll":
        categoria = "PEAJE/PARQUIMETRO"
    elif categoria == "Water":
        categoria = "AGUA"
    elif categoria == "MXCell" and name == "TAEMOVISTAR":
        categoria = ["Tiempo Aire", "MOVISTAR"]
    elif categoria == "MXCell" and name == "TAEUNEFON":
        categoria = ["Tiempo Aire", "UNEFON"]
    elif categoria == "MXCell" and name == "TAEVIRGIN":
        categoria = ["Tiempo Aire", "VIRGIN"]
    elif categoria == "MXCell" and name == "AMIGO SL":
        categoria = ["Tiempo Aire", "AMIGO SL"]
    elif categoria == "MXCell" and name == "TAETelcel":
        categoria = ["Tiempo Aire", "TELCEL"]
    elif categoria == "MXCell" and name == "INTERNET AMIGO":
        categoria = ["Tiempo Aire", "INTERNET AMIGO"]
    elif categoria == "MXCell" and name == "MovistarInternet":
        categoria = ["Tiempo Aire", "MOVISTAR INTERNET"]
    elif categoria == "MXCell" and name == "Bait":
        categoria = ["Tiempo Aire", "BAIT"]
    else:
        categoria = "NO MOSTRAR"
    return categoria
