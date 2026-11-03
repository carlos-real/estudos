"""Roda com:  python -m labqualidade   (de dentro da pasta exemplos)."""

from labqualidade import __version__, faixa_nominal, resumo

print(f"labqualidade {__version__}")
print("Faixa de 25 µm ± 10%:", faixa_nominal(25.0, 10))
print("Resumo:", resumo([25.1, 24.8, 25.3, 24.9]))
