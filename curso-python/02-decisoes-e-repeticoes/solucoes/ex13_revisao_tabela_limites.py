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


def tolerancia_pct(linha: str) -> float | None:
    """Função auxiliar: tolerância padrão da linha, ou None se não existir."""
    match linha:
        case "A" | "B":
            return 5.0
        case "C":
            return 8.0
        case "D":
            return 10.0
        case _:
            return None


def tabela_limites(linhas: str, nominais: list[float]) -> str:
    """Devolve a tabela de limites (texto com várias linhas) por linha e nominal."""
    resultado = ""  # acumulador de TEXTO: começa vazio e vai crescendo com +=
    for caractere in linhas:  # laço de fora: uma volta por linha de produção
        if caractere == " ":
            continue  # espaços são só separadores: pula
        linha = caractere.upper()
        tolerancia = tolerancia_pct(linha)
        if tolerancia is None:
            resultado += f"Linha {linha}: sem tolerância cadastrada\n"
            continue  # nada de nominais para linha desconhecida
        resultado += f"Linha {linha} (±{tolerancia:.0f}%)\n"
        for nominal in nominais:  # laço de dentro: uma volta por nominal
            # Mesma conta do exercício 01.10 (módulo 01).
            margem = nominal * tolerancia / 100
            minimo = nominal - margem
            maximo = nominal + margem
            resultado += f"  {nominal:.2f} µm: {minimo:.2f} a {maximo:.2f}\n"
    return resultado
    # Total de voltas do laço de dentro: (linhas conhecidas) x (nominais).
    # Para 4 linhas e 3 nominais, 12 linhas de limites.
