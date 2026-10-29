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
    for op, peso in zip(ops, pesos):
        totais[op] = totais.get(op, 0.0) + peso

    # Arredondamos só no FIM. Arredondar a cada soma acumula erro.
    # Compreensão de dicionário: mesma chave, valor arredondado.
    return {op: round(total, 2) for op, total in totais.items()}

    # No Python 3.10+, zip(ops, pesos, strict=True) dá ValueError se os
    # tamanhos forem diferentes. Tratar erros com try/except é assunto do
    # módulo 06; por isso aqui conferimos com len().
