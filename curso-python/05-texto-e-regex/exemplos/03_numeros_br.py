"""Exemplo 03 — Números no formato brasileiro (seção 6).

Rode na pasta curso-python:
    python 05-texto-e-regex/exemplos/03_numeros_br.py
"""

TROCA_BR = str.maketrans(",.", ".,")


def br_para_float(texto):
    """'1.250,5' -> 1250.5 (primeiro some o milhar, depois a vírgula vira ponto)."""
    return float(texto.strip().replace(".", "").replace(",", "."))


def float_para_br(valor, casas=2):
    """1250.5 -> '1.250,50'."""
    return f"{valor:,.{casas}f}".translate(TROCA_BR)


print("A armadilha: float('1.250') =", float("1.250"), "(deveria ser 1250!)")
print("Com a conversão certa:", br_para_float("1.250"))
print()

# Texto brasileiro entra -> vira float -> contas em float -> volta a ser texto.
pesos_texto = ["1.250,5", "980,0", "2.040,75"]
pesos = [br_para_float(p) for p in pesos_texto]
total = sum(pesos)
print("Pesos lidos (float):", pesos)
print("Total para o Python:", total)
print("Total para gente:   ", float_para_br(total), "kg")
