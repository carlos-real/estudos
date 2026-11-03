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


def coeficiente_variacao(valores: list[float]) -> float:
    """CV% (desvio amostral / média × 100), com 2 casas."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def resumo_ensaio(valores: list[float]) -> dict[str, float]:
    """Resumo estatístico de um ensaio."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
