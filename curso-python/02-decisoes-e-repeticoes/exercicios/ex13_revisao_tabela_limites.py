"""
Exercício 02.13 — Revisão: tabela de limites por linha
Nível: ★★★

Revisão: este exercício mistura o módulo 02 (laços aninhados, match-case, continue)
com o módulo 01 (cálculo de tolerância, f-strings com :.2f, upper) e com o molde de
função do módulo 00.

Contexto: O supervisor quer uma "cola" impressa com os limites de espessura de cada
linha para os nominais mais produzidos, para pendurar ao lado das extrusoras.

Tolerâncias por linha: A: 5%   B: 5%   C: 8%   D: 10%

Tarefa: implemente `tabela_limites(linhas, nominais)`:
- `linhas` é uma string em que cada caractere é uma linha (ex.: "ACD"). Ignore espaços
  e aceite minúsculas ("a c" equivale a "AC").
- `nominais` é uma lista de espessuras nominais em µm.
- Para cada linha conhecida, gere um cabeçalho e, para cada nominal, uma linha
  recuada com 2 espaços:
      Linha A (±5%)
        20.00 µm: 19.00 a 21.00
        25.00 µm: 23.75 a 26.25
- Para uma linha desconhecida (ex.: "X"), gere só: Linha X: sem tolerância cadastrada
- TODA linha do texto termina com "\\n" (inclusive a última).
- Valores com 2 casas (:.2f); tolerância sem casas (:.0f).

Exemplos:
    >>> print(tabela_limites("a", [20, 25]), end="")
    Linha A (±5%)
      20.00 µm: 19.00 a 21.00
      25.00 µm: 23.75 a 26.25
    >>> tabela_limites("X", [20])
    'Linha X: sem tolerância cadastrada\\n'

Dica: o laço de fora percorre as linhas; o de dentro, os nominais. Use um texto
acumulador (resultado = "" e resultado += ...). Uma função auxiliar com match-case
para a tolerância deixa tudo mais limpo.

Teste com:  python curso.py testar 02 ex13
"""


def tabela_limites(linhas: str, nominais: list[float]) -> str:
    """Devolve a tabela de limites (texto com várias linhas) por linha e nominal."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
