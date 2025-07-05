import re


DDDS_VALIDOS = {
    '11', '12', '13', '14', '15', '16', '17', '18', '19',
    '21', '22', '24', '27', '28',
    '31', '32', '33', '34', '35', '37', '38',
    '41', '42', '43', '44', '45', '46',
    '47', '48', '49',
    '51', '53', '54', '55',
    '61', '62', '64', '63', '65', '66', '67', '68', '69',
    '71', '73', '74', '75', '77', '79',
    '81', '82', '83', '84', '85', '86', '87', '88', '89',
    '91', '92', '93', '94', '95', '96', '97', '98', '99'
}

def validar_telefone(telefone):
    numeros = re.sub(r'\D', '', telefone)

    if numeros.startswith("55"):
        numeros = numeros[2:]

    if len(numeros) != 11:
        return False

    ddd = numeros[:2]
    celular = numeros[2:]

    if ddd not in DDDS_VALIDOS:
        return False

    if not celular.startswith("9"):
        return False

    return True

def formatar_telefone(telefone):
    numeros = re.sub(r'\D', '', telefone)

    if numeros.startswith("55"):
        numeros = numeros[2:]

    if len(numeros) == 11:
        ddd = numeros[:2]
        parte1 = numeros[2:7]
        parte2 = numeros[7:]
        return f"({ddd}) {parte1}-{parte2}"
    
    return telefone


def validar_telefone_final(telefone):
    if not validar_telefone(telefone):
        return None
    return formatar_telefone(telefone)
