"""
Exercício 09.01 — Limites de tolerância (TDD: os testes vêm primeiro)
Nível: ★☆☆

Solução comentada. Veja o enunciado completo em exercicios/ex01_limites_tolerancia.py.
"""


def calcular_limites(nominal: float, tolerancia_pct: float) -> tuple[float, float]:
    """Devolve (mínimo, máximo) de nominal ± tolerancia_pct %."""
    # Validações primeiro ("retorno antecipado"): se a entrada é inválida, nem
    # adianta calcular. Cada regra do enunciado virou um teste e um if aqui.
    if nominal <= 0:
        raise ValueError(f"nominal deve ser maior que zero, recebi {nominal}")
    if tolerancia_pct < 0:
        raise ValueError(f"tolerância não pode ser negativa, recebi {tolerancia_pct}")

    # No ciclo do TDD, a primeira versão "verde" poderia repetir a conta:
    #     return nominal - nominal * tolerancia_pct / 100, nominal + ...
    # No passo de REFATORAR nasce a variável margem, com nome claro e sem
    # repetição. Os testes garantem que nada quebrou nessa mudança.
    margem = nominal * tolerancia_pct / 100
    return nominal - margem, nominal + margem
