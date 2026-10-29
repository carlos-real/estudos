"""
Solução — Exercício 03.02 — Resumo de espessura

Ideia central: as funções embutidas sum, min, max e len trabalham sobre a lista
inteira, sem você escrever nenhum laço.
"""


def resumo_espessura(medicoes: list[float]) -> dict[str, float]:
    """Devolve mínimo, máximo, média e amplitude das medições."""
    # Lista vazia primeiro: min([]) e max([]) dão ValueError, e a média
    # dividiria por zero. Uma lista vazia é falsy, então "if not medicoes" basta.
    if not medicoes:
        return {}

    # Guardamos min e max em variáveis para não percorrer a lista duas vezes
    # cada um (e para o código ficar legível).
    minimo = min(medicoes)
    maximo = max(medicoes)

    return {
        "minimo": minimo,
        "maximo": maximo,
        "media": round(sum(medicoes) / len(medicoes), 2),
        "amplitude": round(maximo - minimo, 2),
    }
