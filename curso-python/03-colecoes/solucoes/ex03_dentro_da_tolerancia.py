"""
Solução — Exercício 03.03 — Dentro da tolerância?

Ideia central: `dict.get` busca sem quebrar o programa quando a chave falta, e
o desempacotamento transforma a tupla (mín, máx) em duas variáveis com nome.
"""


def dentro_da_tolerancia(
    valor: float, linha: str, tolerancias: dict[str, tuple[float, float]]
) -> bool | None:
    """Diz se o valor está na faixa da linha (None se a linha não existe)."""
    # Normalizar a chave ANTES de procurar: " a " vira "A".
    chave = linha.strip().upper()

    # get devolve None se a chave não existe (com [] seria KeyError).
    faixa = tolerancias.get(chave)
    if faixa is None:
        return None

    # Desempacotamento: a tupla (45.0, 55.0) vira duas variáveis.
    minimo, maximo = faixa

    # Comparação encadeada (módulo 02): já devolve True ou False.
    return minimo <= valor <= maximo

    # Alternativa com "in" (também correta):
    #     if chave not in tolerancias:
    #         return None
    #     minimo, maximo = tolerancias[chave]
