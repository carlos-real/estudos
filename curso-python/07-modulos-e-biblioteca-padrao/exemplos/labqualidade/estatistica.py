"""Estatística descritiva usada no laboratório."""

import statistics


def cv_percentual(valores: list[float]) -> float:
    """Coeficiente de variação em %: desvio padrão amostral / média * 100."""
    return statistics.stdev(valores) / statistics.mean(valores) * 100


def resumo(valores: list[float]) -> dict[str, float]:
    """Resumo com n, média, desvio padrão e CV% (arredondados)."""
    return {
        "n": len(valores),
        "media": round(statistics.mean(valores), 3),
        "desvio": round(statistics.stdev(valores), 3),
        "cv": round(cv_percentual(valores), 2),
    }
