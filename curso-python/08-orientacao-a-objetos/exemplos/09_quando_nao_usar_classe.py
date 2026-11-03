"""Quando NÃO usar classe: o mesmo problema, mais simples.

Rode com:  python exemplos/09_quando_nao_usar_classe.py
"""

import statistics


# Exagero: classe sem estado, só para "embrulhar" uma conta
class CalculadoraDeCV:
    def __init__(self) -> None:
        pass

    def calcular(self, valores: list[float]) -> float:
        return statistics.stdev(valores) / statistics.mean(valores) * 100


print("Com classe:", round(CalculadoraDeCV().calcular([25.1, 24.8, 25.3]), 2))


# Simples: uma função resolve (e se testa igual)
def cv_percentual(valores: list[float]) -> float:
    return statistics.stdev(valores) / statistics.mean(valores) * 100


print("Com função:", round(cv_percentual([25.1, 24.8, 25.3]), 2))

# Só para agrupar constantes? Um dicionário (ou um módulo) basta.
NOMINAL_POR_LINHA = {"A": 20.0, "B": 25.0, "C": 40.0, "D": 60.0}
print("Nominal da linha C:", NOMINAL_POR_LINHA["C"])
