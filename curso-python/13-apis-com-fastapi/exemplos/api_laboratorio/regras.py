"""Regras de tolerância. Funções puras: fáceis de testar, sem FastAPI e sem banco."""


def limites(
    tipo: str,
    minimo: float | None,
    maximo: float | None,
    nominal: float | None,
    percentual: float | None,
) -> tuple[float, float]:
    """Devolve (mínimo, máximo) para tolerância por faixa ou por nominal ± %."""
    if tipo == "faixa":
        return minimo, maximo
    folga = nominal * percentual / 100
    return round(nominal - folga, 4), round(nominal + folga, 4)


def dentro(valor: float, minimo: float, maximo: float) -> bool:
    """Os limites fazem parte da faixa: 18,0 está dentro de 18,0 a 22,0."""
    return minimo <= valor <= maximo
