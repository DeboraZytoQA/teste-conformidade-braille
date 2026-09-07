"""
Testes da tabela de sinais contra a norma.

Especificacao de referencia: "Grafia Braille para a Lingua Portuguesa"
(MEC / Instituto Benjamin Constant).

Cada teste aqui compara a implementacao com o que a norma determina,
usando os PONTOS como a norma os descreve. Nao ha valor "esperado"
inventado: todo valor esperado vem do documento.
"""

import pytest

from braille import tabela_braille as tb
from braille.transcritor import (
    CaractereNaoMapeado,
    destranscrever,
    transcrever,
)


# ---------------------------------------------------------------------------
# CT01 - Alfabeto
# ---------------------------------------------------------------------------

ALFABETO_NORMA = [
    ("a", (1,)),            ("b", (1, 2)),          ("c", (1, 4)),
    ("d", (1, 4, 5)),       ("e", (1, 5)),          ("f", (1, 2, 4)),
    ("g", (1, 2, 4, 5)),    ("h", (1, 2, 5)),       ("i", (2, 4)),
    ("j", (2, 4, 5)),       ("k", (1, 3)),          ("l", (1, 2, 3)),
    ("m", (1, 3, 4)),       ("n", (1, 3, 4, 5)),    ("o", (1, 3, 5)),
    ("p", (1, 2, 3, 4)),    ("q", (1, 2, 3, 4, 5)), ("r", (1, 2, 3, 5)),
    ("s", (2, 3, 4)),       ("t", (2, 3, 4, 5)),    ("u", (1, 3, 6)),
    ("v", (1, 2, 3, 6)),    ("w", (2, 4, 5, 6)),    ("x", (1, 3, 4, 6)),
    ("y", (1, 3, 4, 5, 6)), ("z", (1, 3, 5, 6)),
]


@pytest.mark.parametrize("letra, pontos", ALFABETO_NORMA)
def test_alfabeto_segue_a_norma(letra, pontos):
    assert transcrever(letra) == tb.celula(*pontos)


def test_alfabeto_esta_completo():
    assert len(tb.LETRAS) == 26


# ---------------------------------------------------------------------------
# CT02 - Letras com diacriticos
# ---------------------------------------------------------------------------

DIACRITICOS_NORMA = [
    ("ç", (1, 2, 3, 4, 6)),
    ("á", (1, 2, 3, 5, 6)),
    ("é", (1, 2, 3, 4, 5, 6)),
    ("í", (3, 4)),
    ("ó", (3, 4, 6)),
    ("ú", (2, 3, 4, 5, 6)),
    ("â", (1, 6)),
    ("ê", (1, 2, 6)),
    ("ô", (1, 4, 5, 6)),
    ("ã", (3, 4, 5)),
    ("õ", (2, 4, 6)),
    ("à", (1, 2, 4, 6)),
    ("ü", (1, 2, 5, 6)),
]


@pytest.mark.parametrize("letra, pontos", DIACRITICOS_NORMA)
def test_diacriticos_seguem_a_norma(letra, pontos):
    assert transcrever(letra) == tb.celula(*pontos)


def test_letra_acentuada_nao_vira_letra_simples():
    """A cedilha nao pode ser transcrita como um simples 'c'."""
    assert transcrever("ç") != transcrever("c")
    assert transcrever("á") != transcrever("a")


# ---------------------------------------------------------------------------
# CT03 - Sinal indicativo de maiuscula (pontos 4-6)
# ---------------------------------------------------------------------------

def test_maiuscula_recebe_o_sinal_antes_da_letra():
    assert transcrever("A") == tb.celula(4, 6) + tb.celula(1)


def test_minuscula_nao_recebe_sinal():
    assert transcrever("a") == tb.celula(1)


def test_nome_proprio_marca_apenas_a_primeira_letra():
    esperado = tb.celula(4, 6) + tb.LETRAS["r"] + tb.DIACRITICOS["á"]
    assert transcrever("Rá") == esperado


# ---------------------------------------------------------------------------
# CT04 - Sinal de numero (pontos 3-4-5-6)
# ---------------------------------------------------------------------------

def test_numero_recebe_o_sinal_uma_unica_vez():
    esperado = (
        tb.celula(3, 4, 5, 6)
        + tb.LETRAS["a"]  # 1
        + tb.LETRAS["i"]  # 9
        + tb.LETRAS["b"]  # 2
        + tb.LETRAS["b"]  # 2
    )
    assert transcrever("1922") == esperado


def test_sinal_de_numero_reinicia_depois_do_espaco():
    saida = transcrever("1 2")
    assert saida.count(tb.SINAL_NUMERO) == 2


def test_letra_ambigua_apos_numero_recebe_sinal_de_minuscula():
    """
    A norma exige o sinal de letra minuscula (ponto 5) quando uma das
    dez primeiras letras aparece logo depois de um numero. Sem ele,
    "5a" seria lido como "51".
    """
    saida = transcrever("5a")
    assert tb.SINAL_LETRA_MINUSCULA in saida
    assert saida.index(tb.SINAL_LETRA_MINUSCULA) < saida.rindex(tb.LETRAS["a"])


def test_letra_fora_das_dez_primeiras_nao_recebe_sinal():
    assert tb.SINAL_LETRA_MINUSCULA not in transcrever("5x")


# ---------------------------------------------------------------------------
# CT05 - Pontuacao e espacos
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "sinal, pontos",
    [(".", (3,)), (",", (2,)), ("?", (2, 6)), ("!", (2, 3, 5)), ("-", (3, 6))],
)
def test_pontuacao_segue_a_norma(sinal, pontos):
    assert transcrever(sinal) == tb.celula(*pontos)


def test_espaco_entre_palavras_e_preservado():
    assert transcrever("a a").count(" ") == 1


# ---------------------------------------------------------------------------
# CT06 - Tratamento de erro
# ---------------------------------------------------------------------------

def test_caractere_fora_da_tabela_levanta_erro():
    with pytest.raises(CaractereNaoMapeado):
        transcrever("olá @ mundo")


def test_erro_informa_qual_caractere_e_onde():
    with pytest.raises(CaractereNaoMapeado) as erro:
        transcrever("abc€")
    assert erro.value.caractere == "€"
    assert erro.value.posicao == 3


def test_texto_vazio_nao_quebra():
    assert transcrever("") == ""


# ---------------------------------------------------------------------------
# CT07 - Ida e volta
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "frase",
    [
        "O Nilo e um rio grande.",
        "As piramides guardam reis.",
        "Ra era o deus do sol.",
        "O rei era o farao.",
        "Em 1922 acharam a tumba.",
    ],
)
def test_transcrever_e_destranscrever_devolve_o_original(frase):
    assert destranscrever(transcrever(frase)) == frase
