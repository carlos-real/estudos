"""Exemplo 08 — Funções puras x funções com efeitos colaterais.

Rode na pasta 04-funcoes:  python exemplos/08_puras_vs_efeitos.py
"""

# ---------- Versão "faz tudo": difícil de testar e de reaproveitar ----------
reprovadas_do_dia = 0  # estado global


def conferir_e_mostrar(medicoes, minimo, maximo):
    global reprovadas_do_dia  # altera variável de fora: efeito colateral
    medicoes.sort()  # altera a lista de quem chamou: efeito colateral
    fora = [v for v in medicoes if not minimo <= v <= maximo]
    if fora:
        reprovadas_do_dia += 1
    print(f"{len(fora)} fora da faixa: {fora}")  # mostra em vez de devolver


leituras = [50.2, 56.3, 44.1]
conferir_e_mostrar(leituras, 45.0, 55.0)
print("leituras depois:", leituras, "| reprovadas_do_dia:", reprovadas_do_dia)


# ---------- Versão pura: só recebe, calcula e devolve ----------
def valores_fora(medicoes, minimo, maximo):
    """Mesma entrada -> mesma saída. Não lê nem altera nada de fora."""
    return [v for v in medicoes if not minimo <= v <= maximo]


# Testar uma função pura é uma linha:
assert valores_fora([50.2, 56.3, 44.1], 45.0, 55.0) == [56.3, 44.1]
assert valores_fora([], 45.0, 55.0) == []

# ---------- A "casca": os efeitos ficam aqui, na borda do programa ----------
leituras = [50.2, 56.3, 44.1]
fora = valores_fora(leituras, 45.0, 55.0)
print(f"{len(fora)} fora da faixa: {fora}")
print("leituras continuam:", leituras)
