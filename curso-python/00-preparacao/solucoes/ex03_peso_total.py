"""
Solução — Exercício 00.03 — Peso total da carga

Ideia central: a função recebe dois valores (parâmetros), faz uma conta e devolve o
resultado. É o molde de quase todos os exercícios do curso.
"""


def peso_total(peso_bobina_kg: float, quantidade: int) -> float:
    """Devolve o peso total (kg) de `quantidade` bobinas de `peso_bobina_kg` cada."""
    # Multiplicação em Python é `*` (não use x nem ·).
    # Com quantidade 0 a conta já dá 0.0 sozinha: não precisa de nenhum caso especial.
    return peso_bobina_kg * quantidade

    # Por que o teste usa pytest.approx? Porque o computador guarda números com vírgula
    # em binário, e algumas contas saem com um "resto" minúsculo:
    #     12.3 * 3  ->  36.900000000000006
    # Isso não é bug do seu código. O módulo 01 explica e mostra como arredondar.
