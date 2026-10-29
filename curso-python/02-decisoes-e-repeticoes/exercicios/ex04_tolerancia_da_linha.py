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
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
