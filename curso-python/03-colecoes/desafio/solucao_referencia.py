"""Desafio do módulo 03 — Painel de conferência do lote (solução de referência).

Rode na pasta 03-colecoes:  python desafio/solucao_referencia.py

Usa só o que foi visto até o módulo 03: listas, tuplas, dicionários (inclusive
aninhados), conjuntos, compreensões, sorted com key e funções simples (def +
return, o "molde" do módulo 01). Nenhuma função altera os dados recebidos.
"""

# ---------------------------------------------------------------------------
# Dados do dia (no projeto real, viriam da planilha e do e-mail da expedição)
# ---------------------------------------------------------------------------

TOLERANCIAS = {
    "A": {
        "espessura": {"nominal": 50.0, "tol_pct": 10.0},
        "gramatura": {"nominal": 46.0, "tol_pct": 5.0},
        "cof": {"min": 0.15, "max": 0.30},
    },
    "B": {
        "espessura": {"nominal": 20.0, "tol_pct": 8.0},
        "gramatura": {"nominal": 18.5, "tol_pct": 5.0},
        "cof": {"min": 0.20, "max": 0.40},
    },
    "C": {
        "espessura": {"nominal": 35.0, "tol_pct": 10.0},
        "gramatura": {"nominal": 32.0, "tol_pct": 6.0},
        "cof": {"min": 0.15, "max": 0.30},
    },
    "D": {
        "espessura": {"nominal": 70.0, "tol_pct": 7.0},
        "gramatura": {"nominal": 65.0, "tol_pct": 5.0},
        "cof": {"min": 0.10, "max": 0.25},
    },
}

COLUNAS = ("op", "linha", "espessura", "gramatura", "cof", "obs")
PLANILHA = [
    ("OP-5101", "A", 50.4, 46.3, 0.22, ""),
    ("OP-5102", "A", 55.8, 46.9, 0.24, ""),
    ("OP-5103", "B", 20.6, 18.9, 0.42, "COF: liberado"),
    ("OP-5104", "B", 19.1, None, 0.30, ""),
    ("OP-5105", "C", 35.9, 32.4, 0.19, ""),
    ("OP-5106", "C", 31.0, 29.5, 0.33, ""),
    ("OP-5107", "D", 71.2, 66.0, 0.12, ""),
    ("OP-5108", "D", 70.4, 64.1, 0.26, "cof: liberado pela supervisão"),
    ("OP-5109", "A", 47.9, 44.0, 0.16, ""),
    ("OP-5110", "D", 64.9, 61.5, 0.11, ""),
]
AMOSTRAS = [dict(zip(COLUNAS, linha, strict=True)) for linha in PLANILHA]

PEDIDOS = [
    {"op": "OP-5101", "nf": "004501", "peso_kg": 1250.5},
    {"op": "OP-5103", "nf": "004502", "peso_kg": 830.0},
    {"op": "OP-5106", "nf": "004503", "peso_kg": 640.2},
    {"op": "OP-5108", "nf": "004504", "peso_kg": 1105.8},
    {"op": "OP-5104", "nf": "004505", "peso_kg": 412.0},
    {"op": "OP-5120", "nf": "004506", "peso_kg": 300.0},
]

# ---------------------------------------------------------------------------
# Regras
# ---------------------------------------------------------------------------


def faixa(regra):
    """Converte uma regra ({nominal, tol_pct} ou {min, max}) em (mínimo, máximo)."""
    if "nominal" in regra:
        nominal, fator = regra["nominal"], regra["tol_pct"] / 100
        return round(nominal * (1 - fator), 2), round(nominal * (1 + fator), 2)
    return regra["min"], regra["max"]


def conferir(amostra):
    """Devolve uma CÓPIA da amostra com as colunas 'falhas' e 'status'."""
    regras = TOLERANCIAS[amostra["linha"]]
    faltando = [p for p in regras if amostra.get(p) is None]
    if faltando:
        return {**amostra, "falhas": faltando, "status": "INCOMPLETA"}

    falhas = []
    for propriedade, regra in regras.items():
        minimo, maximo = faixa(regra)
        if not minimo <= amostra[propriedade] <= maximo:
            falhas.append(propriedade)

    if not falhas:
        status = "APROVADA"
    elif falhas == ["cof"] and "cof: liberado" in amostra["obs"].lower():
        status = "LIBERADA"
    else:
        status = "REPROVADA"
    return {**amostra, "falhas": falhas, "status": status}


def desvio_pct_espessura(amostra):
    """Desvio percentual da espessura em relação ao nominal da linha."""
    nominal = TOLERANCIAS[amostra["linha"]]["espessura"]["nominal"]
    return round(100 * (amostra["espessura"] - nominal) / nominal, 1)


def pode_emitir(conferida):
    return conferida["status"] in ("APROVADA", "LIBERADA")


# ---------------------------------------------------------------------------
# Saída
# ---------------------------------------------------------------------------


def texto(valor, casas):
    """Formata número; célula vazia vira '-'."""
    # {casas} dentro do formato: o número de casas vem de uma variável.
    return "-" if valor is None else f"{valor:.{casas}f}"


def imprimir_tabela(conferidas):
    print(f"{'OP':<9}{'Linha':<6}{'Esp.':>6}{'Gram.':>7}{'COF':>6}  {'Status':<11}Fora")
    for c in conferidas:
        fora = ", ".join(c["falhas"]) if c["falhas"] else "-"
        print(
            f"{c['op']:<9}{c['linha']:<6}{texto(c['espessura'], 1):>6}"
            f"{texto(c['gramatura'], 1):>7}{texto(c['cof'], 2):>6}  {c['status']:<11}{fora}"
        )


def imprimir_resumo_por_linha(conferidas):
    grupos = {}
    for c in conferidas:
        grupos.setdefault(c["linha"], []).append(c)
    print(f"{'Linha':<6}{'Amostras':>9}{'Liberadas':>10}{'%':>7}{'Esp. média':>12}")
    for linha in sorted(grupos):
        grupo = grupos[linha]
        liberadas = sum(pode_emitir(c) for c in grupo)
        pct = 100 * liberadas / len(grupo)
        media = sum(c["espessura"] for c in grupo) / len(grupo)
        print(f"{linha:<6}{len(grupo):>9}{liberadas:>10}{pct:>6.1f}%{media:>12.2f}")


def imprimir_maiores_desvios(conferidas, quantidade):
    ordenadas = sorted(conferidas, key=lambda c: abs(desvio_pct_espessura(c)), reverse=True)
    for c in ordenadas[:quantidade]:
        print(f"{c['op']} (linha {c['linha']}): {desvio_pct_espessura(c):+.1f}% do nominal")


def imprimir_expedicao(conferidas, pedidos):
    por_op = {c["op"]: c for c in conferidas}
    emitir = [p for p in pedidos if p["op"] in por_op and pode_emitir(por_op[p["op"]])]
    bloqueados = [p for p in pedidos if p["op"] in por_op and not pode_emitir(por_op[p["op"]])]
    sem_resultado = {p["op"] for p in pedidos} - set(por_op)

    peso_total = sum(p["peso_kg"] for p in emitir)
    print(f"Emitir certificado ({len(emitir)} OPs, {peso_total:.1f} kg):")
    for p in emitir:
        status = por_op[p["op"]]["status"]
        print(f"  {p['op']}  NF {p['nf']}  {p['peso_kg']:.1f} kg  [{status}]")
    print("Bloqueadas:")
    for p in bloqueados:
        c = por_op[p["op"]]
        print(f"  {p['op']}  {c['status']}: {', '.join(c['falhas'])}")
    print("Sem resultado no laboratório:", sorted(sem_resultado))


def main():
    conferidas = [conferir(amostra) for amostra in AMOSTRAS]

    print("=" * 60)
    print("PAINEL DE CONFERÊNCIA DO LOTE")
    print("=" * 60)
    imprimir_tabela(conferidas)

    print("\n--- Resumo por linha ---")
    imprimir_resumo_por_linha(conferidas)

    print("\n--- 3 maiores desvios de espessura ---")
    imprimir_maiores_desvios(conferidas, 3)

    print("\n--- Expedição ---")
    imprimir_expedicao(conferidas, PEDIDOS)

    # Prova de que nada foi alterado: as amostras originais não têm 'status'.
    assert all("status" not in amostra for amostra in AMOSTRAS)


main()
