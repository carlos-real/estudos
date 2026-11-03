"""
Solução — Exercício 04.04 — Média com quantos valores vierem

Ideia central: *valores recolhe todos os argumentos posicionais numa TUPLA.
A função trata essa tupla como qualquer coleção (len, sum, for...).
"""


def media(*valores: float) -> float | None:
    """Média de todos os valores recebidos (None se não vier nenhum)."""
    if not valores:  # tupla vazia: ninguém passou nada
        return None
    return sum(valores) / len(valores)


def maior_desvio(nominal: float, *medicoes: float) -> float:
    """Maior |medição − nominal|, com 2 casas (0.0 sem medições)."""
    # O primeiro argumento vai para "nominal"; o RESTO vai para a tupla.
    # max(..., default=0.0) cobre o caso sem medições (módulo 03).
    maior = max((abs(valor - nominal) for valor in medicoes), default=0.0)
    return round(maior, 2)
