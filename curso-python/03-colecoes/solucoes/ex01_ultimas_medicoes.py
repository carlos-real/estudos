"""
Solução — Exercício 03.01 — Últimas medições

Ideia central: fatiamento com índice negativo (`lista[-n:]`) pega "do n-ésimo a
partir do fim até o fim". Fatiar nunca dá IndexError e sempre cria uma lista nova.
"""


def ultimas_medicoes(medicoes: list[float], n: int) -> list[float]:
    """Devolve uma lista nova com as n últimas medições, na ordem original."""
    # Armadilha: -0 é igual a 0, então medicoes[-0:] vira medicoes[0:],
    # que é a lista INTEIRA. Por isso tratamos n <= 0 antes de fatiar.
    if n <= 0:
        return []

    # Se n for maior que len(medicoes), o fatiamento simplesmente para no
    # começo da lista (sem erro). E o resultado já é uma lista nova (cópia),
    # então a lista original nunca é alterada.
    return medicoes[-n:]

    # Alternativa equivalente, sem índice negativo:
    #     inicio = max(len(medicoes) - n, 0)
    #     return medicoes[inicio:]
