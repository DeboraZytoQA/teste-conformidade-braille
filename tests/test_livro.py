"""
Testes do livro digital.

Aqui o alvo nao e mais a tabela, e sim o produto entregue: o arquivo
HTML. Dois grupos de verificacao:

  1. conteudo  - o Braille de cada pagina corresponde mesmo ao texto;
  2. acessibilidade - o HTML tem o que um leitor de tela precisa.
"""

import re
from pathlib import Path

import pytest

from braille.transcritor import destranscrever, transcrever

ARQUIVO_LIVRO = Path(__file__).resolve().parent.parent / "livro-egito-braille.html"

TOTAL_DE_PAGINAS = 9  # capa + 8 paginas


@pytest.fixture(scope="module")
def html():
    return ARQUIVO_LIVRO.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def paginas(html):
    """Extrai os pares texto/braille declarados no livro."""
    encontrados = re.findall(
        r'texto:\s*"(.*?)",\s*braille:\s*"(.*?)"', html
    )
    assert encontrados, "Nenhuma pagina foi encontrada no HTML."
    return encontrados


# ---------------------------------------------------------------------------
# CT08 - Conteudo do livro
# ---------------------------------------------------------------------------

def test_livro_tem_todas_as_paginas(paginas):
    assert len(paginas) == TOTAL_DE_PAGINAS


def test_braille_de_cada_pagina_corresponde_ao_texto(paginas):
    divergentes = [
        texto for texto, braille in paginas if braille != transcrever(texto)
    ]
    assert not divergentes, f"Paginas com Braille incorreto: {divergentes}"


def test_braille_volta_a_ser_o_texto_original(paginas):
    for texto, braille in paginas:
        assert destranscrever(braille) == texto


def test_nenhuma_linha_passa_de_40_celulas(paginas):
    """
    40 celulas e a largura de uma linha Braille impressa. Manter esse
    limite deixa o livro pronto para virar versao em relevo.
    """
    longas = [texto for texto, braille in paginas if len(braille) > 40]
    assert not longas, f"Linhas longas demais: {longas}"


def test_frases_sao_curtas_para_leitor_iniciante(paginas):
    for texto, _ in paginas:
        assert len(texto.split()) <= 7, f"Frase longa demais: {texto}"


# ---------------------------------------------------------------------------
# CT09 - Acessibilidade do HTML
# ---------------------------------------------------------------------------

def test_idioma_da_pagina_esta_declarado(html):
    assert 'lang="pt-BR"' in html


def test_cada_pagina_tem_uma_ilustracao(html):
    assert html.count('class="cena"') == TOTAL_DE_PAGINAS


def test_toda_ilustracao_tem_descricao_para_leitor_de_tela(html):
    cenas = re.findall(r'<svg class="cena"[^>]*>', html)
    sem_descricao = [cena for cena in cenas if "aria-label=" not in cena]
    assert not sem_descricao, "Ha ilustracao sem aria-label."


def test_descricoes_das_ilustracoes_sao_uteis(html):
    """Uma descricao de duas palavras nao ajuda ninguem."""
    descricoes = re.findall(r'<svg class="cena"[^>]*aria-label="(.*?)"', html)
    assert len(descricoes) == TOTAL_DE_PAGINAS
    for descricao in descricoes:
        assert len(descricao.split()) >= 8, f"Descricao curta: {descricao}"


def test_braille_visual_fica_oculto_para_o_leitor_de_tela(html):
    """
    Os pontos desenhados sao uma representacao visual. Se o leitor de
    tela tentar ler, sai ruido. O texto real ja esta na pagina.
    """
    faixa = re.search(r'<svg id="braille"[^>]*>', html)
    assert faixa is not None
    assert 'aria-hidden="true"' in faixa.group(0)


def test_troca_de_pagina_e_anunciada(html):
    """
    Ao virar a pagina, quem usa leitor de tela precisa ser avisado do
    novo texto. Sem uma regiao viva, a troca acontece em silencio.
    """
    assert re.search(r'id="texto"[^>]*aria-live="polite"', html) or re.search(
        r'aria-live="polite"[^>]*id="texto"', html
    ), "O texto da pagina nao esta em uma regiao aria-live."


def test_navegacao_funciona_pelo_teclado(html):
    assert "ArrowRight" in html and "ArrowLeft" in html


def test_foco_do_teclado_e_visivel(html):
    assert "focus-visible" in html
