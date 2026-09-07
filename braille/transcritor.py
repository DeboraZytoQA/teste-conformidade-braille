"""
Transcritor de texto em portugues para Braille (grafia integral).

Grafia integral significa letra a letra, sem abreviaturas. E a grafia
usada em livros para leitores iniciantes.
"""

from braille import tabela_braille as tb


class CaractereNaoMapeado(ValueError):
    """Levantado quando o texto contem um caractere fora da tabela."""

    def __init__(self, caractere: str, posicao: int):
        self.caractere = caractere
        self.posicao = posicao
        super().__init__(
            f"Caractere nao mapeado {caractere!r} (U+{ord(caractere):04X}) "
            f"na posicao {posicao}."
        )


_MAPA = tb.tabela_completa()


def transcrever(texto: str) -> str:
    """
    Converte uma string em portugues para celulas Braille Unicode.

    Regras aplicadas:
      - letra maiuscula recebe o sinal de maiuscula (pontos 4-6) antes dela;
      - uma sequencia de algarismos recebe o sinal de numero (3-4-5-6) uma
        unica vez, no inicio;
      - letra de "a" a "j" logo apos um numero recebe o sinal de letra
        minuscula (ponto 5), para nao ser lida como algarismo;
      - espacos e quebras de linha sao preservados.
    """
    saida = []
    modo_numero = False

    for posicao, caractere in enumerate(texto):
        if caractere in ("\n", "\r"):
            saida.append(caractere)
            modo_numero = False
            continue

        if caractere == " ":
            saida.append(tb.ESPACO)
            modo_numero = False
            continue

        if caractere.isdigit():
            if not modo_numero:
                saida.append(tb.SINAL_NUMERO)
                modo_numero = True
            saida.append(tb.DIGITOS[caractere])
            continue

        minuscula = caractere.lower()

        if minuscula in _MAPA:
            if modo_numero and minuscula in tb.LETRAS_AMBIGUAS_APOS_NUMERO:
                saida.append(tb.SINAL_LETRA_MINUSCULA)
            if caractere.isupper():
                saida.append(tb.SINAL_MAIUSCULA)
            saida.append(_MAPA[minuscula])
            modo_numero = False
            continue

        raise CaractereNaoMapeado(caractere, posicao)

    return "".join(saida)


# ---------------------------------------------------------------------------
# Transcricao reversa - existe para permitir teste de ida e volta
# ---------------------------------------------------------------------------

_MAPA_REVERSO = {celula: char for char, celula in _MAPA.items()}
_DIGITO_REVERSO = {celula: char for char, celula in tb.DIGITOS.items()}


def destranscrever(braille: str) -> str:
    """
    Converte celulas Braille de volta para texto.

    Usado nos testes de ida e volta. Nao cobre todos os casos da norma:
    serve para validar que a transcricao nao perde informacao.
    """
    saida = []
    indice = 0
    modo_numero = False
    proxima_maiuscula = False

    while indice < len(braille):
        celula = braille[indice]

        if celula in ("\n", "\r", " "):
            saida.append(celula)
            modo_numero = False
            indice += 1
            continue

        if celula == tb.SINAL_MAIUSCULA:
            proxima_maiuscula = True
            indice += 1
            continue

        if celula == tb.SINAL_NUMERO:
            modo_numero = True
            indice += 1
            continue

        if celula == tb.SINAL_LETRA_MINUSCULA:
            modo_numero = False
            indice += 1
            continue

        if modo_numero and celula in _DIGITO_REVERSO:
            saida.append(_DIGITO_REVERSO[celula])
            indice += 1
            continue

        if celula in _MAPA_REVERSO:
            letra = _MAPA_REVERSO[celula]
            saida.append(letra.upper() if proxima_maiuscula else letra)
            proxima_maiuscula = False
            modo_numero = False
            indice += 1
            continue

        raise ValueError(f"Celula desconhecida na posicao {indice}: {celula!r}")

    return "".join(saida)
