# Relatório de testes

Execução completa da suíte sobre a versão entregue do livro.

## Resumo

- Total de testes: 75
- Passando: 75
- Falhando: 0
- Defeitos encontrados durante o desenvolvimento: 1 (DEF-01, corrigido)

## Cobertura por grupo

| Grupo | Casos | Alvo |
| --- | --- | --- |
| CT01 | 27 | Alfabeto completo |
| CT02 | 15 | Letras com diacríticos |
| CT03 | 3 | Sinal de maiúscula |
| CT04 | 4 | Sinal de número e letra ambígua |
| CT05 | 6 | Pontuação e espaços |
| CT06 | 3 | Caractere fora da tabela |
| CT07 | 5 | Ida e volta |
| CT08 | 5 | Conteúdo das 9 páginas |
| CT09 | 7 | Acessibilidade do HTML |

## DEF-01 — Virar a página não é anunciado para o leitor de tela

| Campo | Conteúdo |
| --- | --- |
| Severidade | Alta |
| Encontrado por | `test_troca_de_pagina_e_anunciada` |
| Encontrado em | Primeira versão do livro |
| Status | Corrigido |

**Passos para reproduzir**

1. Abrir o livro com um leitor de tela ativo.
2. Acionar o botão "Avançar".
3. Observar o que é anunciado.

**Resultado obtido**
A página muda visualmente. Nada é anunciado. O leitor de tela permanece em
silêncio até o usuário navegar manualmente até o texto.

**Resultado esperado**
O texto da nova página é anunciado assim que a página é trocada.

**Correção aplicada**
`aria-live="polite"` no parágrafo do texto. Removido o `aria-live` do contador
para evitar anúncio duplicado.

## Fora do escopo desta suíte

- Teste com leitor de tela real (NVDA, VoiceOver, TalkBack).
- Teste com pessoa cega, que é o único que valida a experiência de leitura.
- Contraste medido com ferramenta de acessibilidade.
- Teste em versão impressa em relevo.

Testes automatizados cobrem o que é verificável no código. A validação final de
um material acessível é sempre com quem vai usar.
