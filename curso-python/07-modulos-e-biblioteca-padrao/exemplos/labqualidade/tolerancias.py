"""Regras de tolerância: faixa fixa (mín/máx) e nominal ± percentual."""


def faixa_nominal(nominal: float, percentual: float) -> tuple[float, float]:
    """Devolve (mínimo, máximo) para nominal ± percentual.

    >>> faixa_nominal(25.0, 10)
    (22.5, 27.5)
    """
    margem = nominal * percentual / 100
    return round(nominal - margem, 4), round(nominal + margem, 4)


def dentro_da_faixa(valor: float, minimo: float, maximo: float) -> bool:
    """True se minimo <= valor <= maximo (limites inclusos)."""
    return minimo <= valor <= maximo
