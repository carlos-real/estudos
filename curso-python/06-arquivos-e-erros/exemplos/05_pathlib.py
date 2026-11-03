"""Exemplo 05 — Caminhos e pastas com pathlib (seção 7).

Rode na pasta curso-python:
    python 06-arquivos-e-erros/exemplos/05_pathlib.py
"""

from pathlib import Path

PASTA_DO_SCRIPT = Path(__file__).resolve().parent
LAUDOS = PASTA_DO_SCRIPT.parent / "dados" / "laudos"

regras = PASTA_DO_SCRIPT.parent / "dados" / "regras_tolerancia.json"
print("name  :", regras.name)
print("stem  :", regras.stem)
print("suffix:", regras.suffix)
print("existe?", regras.exists(), "| é arquivo?", regras.is_file())

print(f"\nConteúdo de {LAUDOS.name}/:")
for item in sorted(LAUDOS.iterdir()):
    tipo = "CSV " if item.suffix.lower() == ".csv" else "    "
    print(f"  {tipo}{item.name:<22} {item.stat().st_size:>5} bytes")

csvs = sorted(p.name for p in LAUDOS.iterdir() if p.suffix.lower() == ".csv")
print("\nSó as planilhas CSV:", csvs)
