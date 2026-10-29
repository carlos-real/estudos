"""
Solução — Exercício 03.07 — Peso total por OP

Ideia central: zip junta duas "colunas" em pares; o dicionário ACUMULA o total
de cada chave (é o mesmo padrão da contagem, só que somando pesos).
"""


def pesos_por_op(ops: list[str], pesos: list[float]) -> dict[str, float]:
    """Soma os pesos de cada OP (arredondados em 2 casas)."""
    # zip cortaria a lista maior sem avisar. Conferir o tamanho é validação
    # de dados (módulo 02): melhor recusar do que somar errado.
    if len(ops) != len(pesos):
        return {}

    totais: dict[str, float] = {}
    # strict=True (Python 3.10+) faz o zip reclamar se os tamanhos forem
    # diferentes. Aqui isso nunca acontece, pois já conferimos acima; é uma
    # rede de segurança (e o ruff pede que você deixe a intenção explícita).
    for op, peso in zip(ops, pesos, strict=True):
        totais[op] = totais.get(op, 0.0) + peso

    # Arredondamos só no FIM. Arredondar a cada soma acumula erro.
    # Compreensão de dicionário: mesma chave, valor arredondado.
    return {op: round(total, 2) for op, total in totais.items()}

    # Por que não confiar só no strict=True? Porque ele dá ValueError (o
    # programa para), e tratar erros com try/except é assunto do módulo 06.
    # Conferir com len() deixa a função devolver {} de forma controlada.
