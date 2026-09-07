"""
Tabela de sinais Braille para a lingua portuguesa.

Fonte normativa: "Grafia Braille para a Lingua Portuguesa"
(MEC / Instituto Benjamin Constant).

Cada celula Braille tem 6 pontos, numerados assim:

    1 . . 4
    2 . . 5
    3 . . 6

No Unicode, o bloco "Braille Patterns" comeca em U+2800 e cada ponto
corresponde a um bit. Por isso a tabela abaixo e escrita em PONTOS
(que e como a norma descreve os sinais) e o caractere e calculado.
Isso evita erro de digitacao e mantem uma unica fonte de verdade.
"""

BASE_UNICODE_BRAILLE = 0x2800

_BIT_DO_PONTO = {1: 0x01, 2: 0x02, 3: 0x04, 4: 0x08, 5: 0x10, 6: 0x20}


def celula(*pontos: int) -> str:
    """Converte uma lista de pontos (ex.: celula(1, 2, 4)) na celula Unicode."""
    if not pontos:
        return chr(BASE_UNICODE_BRAILLE)  # celula vazia (espaco Braille)
    valor = 0
    for ponto in pontos:
        if ponto not in _BIT_DO_PONTO:
            raise ValueError(f"Ponto invalido: {ponto}. Use valores de 1 a 6.")
        valor |= _BIT_DO_PONTO[ponto]
    return chr(BASE_UNICODE_BRAILLE + valor)


# ---------------------------------------------------------------------------
# Alfabeto
# ---------------------------------------------------------------------------

LETRAS = {
    "a": celula(1),
    "b": celula(1, 2),
    "c": celula(1, 4),
    "d": celula(1, 4, 5),
    "e": celula(1, 5),
    "f": celula(1, 2, 4),
    "g": celula(1, 2, 4, 5),
    "h": celula(1, 2, 5),
    "i": celula(2, 4),
    "j": celula(2, 4, 5),
    "k": celula(1, 3),
    "l": celula(1, 2, 3),
    "m": celula(1, 3, 4),
    "n": celula(1, 3, 4, 5),
    "o": celula(1, 3, 5),
    "p": celula(1, 2, 3, 4),
    "q": celula(1, 2, 3, 4, 5),
    "r": celula(1, 2, 3, 5),
    "s": celula(2, 3, 4),
    "t": celula(2, 3, 4, 5),
    "u": celula(1, 3, 6),
    "v": celula(1, 2, 3, 6),
    "w": celula(2, 4, 5, 6),
    "x": celula(1, 3, 4, 6),
    "y": celula(1, 3, 4, 5, 6),
    "z": celula(1, 3, 5, 6),
}

# ---------------------------------------------------------------------------
# Letras com diacriticos
# ---------------------------------------------------------------------------

DIACRITICOS = {
    "ç": celula(1, 2, 3, 4, 6),
    "á": celula(1, 2, 3, 5, 6),
    "é": celula(1, 2, 3, 4, 5, 6),
    "í": celula(3, 4),
    "ó": celula(3, 4, 6),
    "ú": celula(2, 3, 4, 5, 6),
    "â": celula(1, 6),
    "ê": celula(1, 2, 6),
    "ô": celula(1, 4, 5, 6),
    "ã": celula(3, 4, 5),
    "õ": celula(2, 4, 6),
    "à": celula(1, 2, 4, 6),
    "è": celula(2, 3, 4, 6),
    "ì": celula(1, 4, 6),
    "ù": celula(1, 5, 6),
    "ü": celula(1, 2, 5, 6),
    "ñ": celula(1, 2, 4, 5, 6),
}

# ---------------------------------------------------------------------------
# Pontuacao e sinais acessorios
# ---------------------------------------------------------------------------

PONTUACAO = {
    ",": celula(2),
    ";": celula(2, 3),
    ":": celula(2, 5),
    ".": celula(3),
    "?": celula(2, 6),
    "!": celula(2, 3, 5),
    '"': celula(2, 3, 6),
    "*": celula(3, 5),
    "-": celula(3, 6),
    "º": celula(3, 5, 6),
    "ª": celula(4, 5),
}

# ---------------------------------------------------------------------------
# Sinais exclusivos do sistema Braille
# ---------------------------------------------------------------------------

SINAL_MAIUSCULA = celula(4, 6)
SINAL_NUMERO = celula(3, 4, 5, 6)
SINAL_LETRA_MINUSCULA = celula(5)
ESPACO = " "

# Os algarismos usam as celulas das dez primeiras letras, precedidas
# do sinal de numero.
DIGITOS = {
    "1": LETRAS["a"],
    "2": LETRAS["b"],
    "3": LETRAS["c"],
    "4": LETRAS["d"],
    "5": LETRAS["e"],
    "6": LETRAS["f"],
    "7": LETRAS["g"],
    "8": LETRAS["h"],
    "9": LETRAS["i"],
    "0": LETRAS["j"],
}

# As dez primeiras letras exigem o sinal de letra minuscula quando
# aparecem logo depois de um numero (norma, cap. II).
LETRAS_AMBIGUAS_APOS_NUMERO = set("abcdefghij")


def tabela_completa() -> dict:
    """Devolve o mapa char -> celula de tudo que e transcrito diretamente."""
    mapa = {}
    mapa.update(LETRAS)
    mapa.update(DIACRITICOS)
    mapa.update(PONTUACAO)
    return mapa
