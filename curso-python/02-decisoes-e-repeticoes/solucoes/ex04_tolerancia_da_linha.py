"""
Exercício 02.04 — Tolerância da linha
Nível: ★☆☆

Contexto: No projeto final, cada linha de produção tem uma tolerância padrão de
espessura, usada quando a OP não tem especificação própria:
    linha A: 5%    linha B: 5%    linha C: 8%    linha D: 10%

Tarefa: implemente `tolerancia_da_linha(linha)`, que devolve a tolerância (float) da
linha informada, ou None se a linha não existir.
- Ignore espaços nas pontas e maiúsculas/minúsculas (" b " vale como "B").
- Use match-case.

Exemplos:
    >>> tolerancia_da_linha("A")
    5.0
    >>> tolerancia_da_linha(" d ")
    10.0
    >>> print(tolerancia_da_linha("E"))
    None

Dica: case "A" | "B": junta dois casos com a mesma resposta. E case _: pega "o resto".
O tipo de retorno `float | None` significa "um float ou None".

Teste com:  python curso.py testar 02 ex04
"""


def tolerancia_da_linha(linha: str) -> float | None:
    """Devolve a tolerância (%) da linha A–D, ou None se a linha não existe."""
    # Normalizar ANTES de comparar: assim " b " e "B" caem no mesmo case.
    match linha.strip().upper():
        case "A" | "B":  # o | junta casos com a mesma resposta
            return 5.0
        case "C":
            return 8.0
        case "D":
            return 10.0
        case _:  # "qualquer outra coisa", como o else de um if
            return None

    # A mesma lógica com if/elif:
    #     codigo = linha.strip().upper()
    #     if codigo == "A" or codigo == "B":
    #         return 5.0
    #     elif codigo == "C":
    #         ...
    # No módulo 03 você verá um jeito ainda melhor para tabelas assim: o dicionário.
