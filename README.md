# Livro digital em Braille teste contra especificação

Livro infantil sobre o Egito Antigo, em letra ampliada e em Braille, com as
ilustrações desenhadas em SVG. O livro é um arquivo HTML único, que abre em
qualquer navegador sem instalação.

**[Ler o livro no navegador](https://deborazytoqa.github.io/teste-conformidade-braille/livro-egito-braille.html)**

O que este repositório mostra não é o livro. É **como o livro foi verificado**.

## O problema de teste

Braille não é decoração. Se uma célula estiver errada, o leitor cego lê outra
palavra — e não tem como desconfiar, porque não existe uma segunda versão para
comparar. Não dá para "olhar e ver se ficou bom": a única referência válida é a
norma.

A especificação usada é a **Grafia Braille para a Língua Portuguesa**
(MEC / Instituto Benjamin Constant). Todo valor esperado nos testes vem dela,
descrito em pontos, como a norma descreve. Nenhum valor esperado foi inventado
a partir da implementação.

## O que é verificado

| Grupo | O que cobre | Por que importa |
| --- | --- | --- |
| CT01 | As 26 letras do alfabeto | Base de tudo |
| CT02 | Letras com diacríticos: ç, á, ã, ê, õ… | É onde o português quebra tabelas feitas para o inglês |
| CT03 | Sinal indicativo de maiúscula, pontos 4-6 | Sem ele, nomes próprios somem |
| CT04 | Sinal de número, pontos 3-4-5-6 | Os algarismos reusam as células das letras a–j |
| CT05 | Pontuação e espaços | Frase sem ponto final vira frase sem fim |
| CT06 | Caractere fora da tabela | O transcritor precisa falhar alto, não emitir célula errada |
| CT07 | Ida e volta: texto → Braille → texto | Prova que nada se perde no caminho |
| CT08 | As 9 páginas do livro entregue | Verifica o produto, não só a biblioteca |
| CT09 | Acessibilidade do HTML | O livro precisa funcionar com leitor de tela |

### O teste de ida e volta

É o mais barato e o que mais pega defeito aqui. Transcrever e destranscrever
tem que devolver exatamente a frase original. Se uma célula estiver trocada, o
caminho de volta entrega outra palavra e o teste acusa — sem precisar de uma
tabela de valores esperados escrita à mão para cada frase.

### O caso mais interessante da norma

A norma exige o sinal de letra minúscula, ponto 5, quando uma das dez primeiras
letras do alfabeto aparece logo depois de um número. Sem esse sinal, `5a` é lido
como `51`, porque o algarismo 1 e a letra `a` são a mesma célula. É o tipo de
regra que só aparece lendo a especificação, nunca testando por intuição.

## Defeito encontrado

**DEF-01 — Virar a página não é anunciado para o leitor de tela**

- **Severidade:** alta. Em um livro que se propõe acessível, é o fluxo principal.
- **Como apareceu:** `test_troca_de_pagina_e_anunciada` falhou.
- **Comportamento:** ao avançar a página, o texto era substituído no DOM sem
  nenhuma região viva. A tela mudava; o leitor de tela seguia em silêncio.
- **Causa:** o parágrafo do texto não estava marcado como `aria-live`. O único
  `aria-live` da página estava no contador, que anuncia "Página 3 de 8" mas não
  o conteúdo.
- **Correção:** `aria-live="polite"` movido para o parágrafo do texto, e removido
  do contador para não haver anúncio duplicado.
- **Status:** corrigido, teste passando.

O defeito estava na primeira versão do livro. Foi encontrado pelo teste, não por
revisão visual — a página parecia perfeita na tela.

## Limitações conhecidas

Documentadas de propósito, não escondidas:

- **Palavra inteira em maiúsculas** recebe o sinal 4-6 letra por letra. A norma
  prevê tratamento próprio para esse caso. Como o livro não usa palavras em
  caixa alta, ficou fora do escopo.
- **Grafia integral apenas**, sem abreviaturas. É a grafia correta para leitor
  iniciante, que é o público do livro.
- **Testes de acessibilidade são estáticos**, feitos sobre o HTML. Não substituem
  teste com leitor de tela real (NVDA, VoiceOver) nem com pessoa cega. Cobrem o
  que dá para automatizar; o resto continua sendo teste manual.
- **Na tela, o Braille é visual.** Quem lê com os dedos precisa de relevo. Os
  pontos aqui servem para quem enxerga acompanhar, e como base para uma versão
  impressa em relevo.

## Como rodar

```bash
pip install -r requirements.txt
python -m pytest -v
```

Para ler o livro, abra `livro-egito-braille.html` no navegador.

## Estrutura

```
.
├── livro-egito-braille.html   # o livro
├── braille/
│   ├── tabela_braille.py      # sinais descritos em pontos, como na norma
│   └── transcritor.py         # texto → Braille e Braille → texto
├── tests/
│   ├── test_tabela_braille.py # CT01 a CT07
│   └── test_livro.py          # CT08 e CT09
└── docs/
    └── relatorio-de-testes.md
```
