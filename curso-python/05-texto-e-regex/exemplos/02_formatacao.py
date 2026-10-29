"""Exemplo 02 — Formatação avançada com f-strings (seção 5).

Rode na pasta curso-python:
    python 05-texto-e-regex/exemplos/02_formatacao.py
"""

valor = 1250.5
print(f"[{valor:,.2f}]  [{valor:12.1f}]  [{valor:*>12,.2f}]")
print(f"[{'OP':<6}]  [{'OP':>6}]  [{'OP':^6}]")
print(f"{42:06d}  {0.987:.1%}  {3.5:+.1f}")

espessura = 25.4
print(f"{espessura=}")  # depuração: mostra nome e valor

largura = 10
casas = 3
print(f"[{'COF':>{largura}}]  {0.21:.{casas}f}")

# Exemplo resolvido: tabela alinhada de medições.
medicoes = [
    ("Espessura", 25.4, "µm"),
    ("Gramatura", 23.1, "g/m²"),
    ("COF estático", 0.21, "-"),
]
print()
print(f"{'Ensaio':<14}{'Valor':>8}  Unidade")
print("-" * 31)
for ensaio, medida, unidade in medicoes:
    print(f"{ensaio:<14}{medida:>8.2f}  {unidade}")
