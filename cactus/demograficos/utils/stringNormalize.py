def normalize(string):
    """_summary_

    Args:
        string (string):Cadena de texto con acentos.

    Returns:
        string: La misma cadena de texto sin acentos.
    """
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        string = string.replace(a, b).replace(a.upper(), b.upper())
    return string
