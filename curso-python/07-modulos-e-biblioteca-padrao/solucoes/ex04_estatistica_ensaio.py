"""
Exercício 07.04 — Estatística de um ensaio
Nível: ★☆☆

Contexto: No ensaio de espessura você mede vários pontos da bobina. O laudo pede
média, mediana, desvio padrão e o coeficiente de variação (CV%), que diz se a
espessura está uniforme: CV% = desvio padrão / média × 100.

Tarefa:
1. `coeficiente_variacao(valores)` devolve o CV% com DESVIO AMOSTRAL
   (statistics.stdev, o mesmo DESVPAD.A do Excel), arredondado com round(..., 2).
   Levante ValueError se houver menos de 2 valores ou se a média for zero.
2. `resumo_ensaio(valores)` devolve um dicionário com as chaves:
   "n" (int), "media", "mediana", "desvio", "minimo", "maximo" (arredondados com
   round(..., 3)) e "cv" (arredondado com round(..., 2)).
   Levante ValueError se houver menos de 2 valores.

Exemplos:
    >>> coeficiente_variacao([25.1, 24.8, 25.3, 24.9, 25.4, 25.0])
    0.92
    >>> resumo_ensaio([10.0, 12.0])["desvio"]
    1.414

Dica: import statistics; use statistics.mean, statistics.median e statistics.stdev.

Teste com:  python curso.py testar 07 ex04
"""

import statistics


def coeficiente_variacao(valores: list[float]) -> float:
    """CV% (desvio amostral / média × 100), com 2 casas."""
    if len(valores) < 2:
        # stdev já daria StatisticsError (que é um tipo de ValueError), mas uma
        # mensagem nossa, em português, ajuda quem usa a função.
        raise ValueError("São necessários pelo menos 2 valores para o CV")
    media = statistics.mean(valores)
    if media == 0:
        raise ValueError("Média zero: o CV não é definido")
    return round(statistics.stdev(valores) / media * 100, 2)


def resumo_ensaio(valores: list[float]) -> dict[str, float]:
    """Resumo estatístico de um ensaio."""
    if len(valores) < 2:
        raise ValueError("São necessários pelo menos 2 valores")
    # Arredondar só na SAÍDA: as contas usam os valores completos.
    return {
        "n": len(valores),
        "media": round(statistics.mean(valores), 3),
        "mediana": round(statistics.median(valores), 3),
        "desvio": round(statistics.stdev(valores), 3),
        "minimo": round(min(valores), 3),
        "maximo": round(max(valores), 3),
        "cv": coeficiente_variacao(valores),  # reaproveita a função acima
    }
