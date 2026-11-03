"""Exemplo 02 — Parâmetros posicionais, nomeados e valores padrão.

Rode na pasta 04-funcoes:  python exemplos/02_parametros.py
"""


def limites(nominal, tol_pct=10.0, casas=2):
    """Devolve (mínimo, máximo) para nominal ± tol_pct %."""
    fator = tol_pct / 100
    return round(nominal * (1 - fator), casas), round(nominal * (1 + fator), casas)


print(limites(50.0))  # usa os padrões
print(limites(46.0, 5.0))  # posicional
print(limites(46.0, tol_pct=5.0))  # nomeado: mais legível
print(limites(nominal=20.0, casas=1, tol_pct=8.0))  # nomeados em qualquer ordem


def formatar(valor, *, casas=1, unidade="µm"):
    """Tudo depois do * só pode ser passado por nome."""
    return f"{valor:.{casas}f} {unidade}"


print(formatar(50.24))
print(formatar(0.2234, casas=3, unidade="(COF)"))
