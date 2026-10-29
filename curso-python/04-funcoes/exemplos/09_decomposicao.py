"""Exemplo 09 — Decomposição: do "funcionão" a funções pequenas e testáveis.

Rode na pasta 04-funcoes:  python exemplos/09_decomposicao.py
"""

NOMINAIS = {"A": (50.0, 10.0), "B": (20.0, 8.0)}  # linha -> (nominal, tol %)
AMOSTRAS = [
    {"op": "OP-4512", "linha": "A", "medicoes": [50.2, 49.8, 51.0]},
    {"op": "OP-4513", "linha": "B", "medicoes": [20.1, 22.3, 19.0]},
    {"op": "OP-4514", "linha": "A", "medicoes": [44.0, 50.3]},
]


# ---------------- ANTES: uma função que faz tudo ----------------
def relatorio_monolitico(amostras, nominais):
    linhas = []
    aprovadas = 0
    for amostra in amostras:
        nominal, pct = nominais[amostra["linha"]]
        minimo = round(nominal * (1 - pct / 100), 2)
        maximo = round(nominal * (1 + pct / 100), 2)
        fora = 0
        for valor in amostra["medicoes"]:
            if valor < minimo or valor > maximo:
                fora += 1
        media = sum(amostra["medicoes"]) / len(amostra["medicoes"])
        if fora == 0:
            status = "APROVADA"
            aprovadas += 1
        else:
            status = "REPROVADA"
        linhas.append(
            f"{amostra['op']} ({amostra['linha']}): média {media:.2f} µm, "
            f"{fora} fora -> {status}"
        )
    linhas.append(f"Turno: {aprovadas}/{len(amostras)} OPs aprovadas")
    return linhas


# ---------------- DEPOIS: cada função faz uma coisa ----------------
def calcular_limites(nominal, tol_pct):
    """(mínimo, máximo) para nominal ± tol_pct %."""
    fator = tol_pct / 100
    return round(nominal * (1 - fator), 2), round(nominal * (1 + fator), 2)


def contar_fora(medicoes, limites):
    """Quantas medições estão fora dos limites."""
    minimo, maximo = limites
    return sum(1 for valor in medicoes if not minimo <= valor <= maximo)


def media(valores):
    """Média simples."""
    return sum(valores) / len(valores)


def conferir_amostra(amostra, nominais):
    """Resume uma amostra num dicionário: op, linha, média, fora e status."""
    limites = calcular_limites(*nominais[amostra["linha"]])
    fora = contar_fora(amostra["medicoes"], limites)
    return {
        "op": amostra["op"],
        "linha": amostra["linha"],
        "media": media(amostra["medicoes"]),
        "fora": fora,
        "status": "APROVADA" if fora == 0 else "REPROVADA",
    }


def formatar_linha(conferencia):
    """Texto de uma amostra conferida."""
    c = conferencia
    return (
        f"{c['op']} ({c['linha']}): média {c['media']:.2f} µm, "
        f"{c['fora']} fora -> {c['status']}"
    )


def formatar_rodape(conferencias):
    """Texto final com o total de aprovadas."""
    aprovadas = sum(1 for c in conferencias if c["status"] == "APROVADA")
    return f"Turno: {aprovadas}/{len(conferencias)} OPs aprovadas"


def gerar_relatorio(amostras, nominais):
    """A 'receita': só junta as funções de baixo."""
    conferencias = [conferir_amostra(a, nominais) for a in amostras]
    return [formatar_linha(c) for c in conferencias] + [formatar_rodape(conferencias)]


# Cada peça testada sozinha (uma linha cada):
assert calcular_limites(50.0, 10.0) == (45.0, 55.0)
assert contar_fora([44.0, 50.3], (45.0, 55.0)) == 1
assert media([1.0, 2.0]) == 1.5

# A versão nova dá EXATAMENTE o mesmo resultado que a antiga:
assert gerar_relatorio(AMOSTRAS, NOMINAIS) == relatorio_monolitico(AMOSTRAS, NOMINAIS)

for linha in gerar_relatorio(AMOSTRAS, NOMINAIS):
    print(linha)
